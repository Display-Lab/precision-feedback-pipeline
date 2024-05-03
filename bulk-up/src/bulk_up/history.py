import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd
import requests

# Define your OIDC Google Cloud service endpoint
ENDPOINT_URL = os.environ.setdefault(
    # "ENDPOINT_URL", "https://pfp.test.app.med.umich.edu/createprecisionfeedback"
    "ENDPOINT_URL",
    "http://localhost:8000/createprecisionfeedback/",
)

from dateutil.relativedelta import relativedelta

# Path to the directory containing input files
INPUT_DIR = os.environ.setdefault("INPUT_DIR", "")
WORKERS = int(os.environ.setdefault("WORKERS", "1"))
START = int(os.getenv("START", "0"))
END = int(os.getenv("END", "10"))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", INPUT_DIR)
LATEST_HISTORY_MONTH = os.environ.get("CURRENT_MONTH", None)
DURATION = int(os.getenv("DURATION", "1"))

candidate_df: pd.DataFrame = pd.DataFrame()
response_df: pd.DataFrame = pd.DataFrame()
lock = threading.Lock()
months_range: list[datetime] = []


def extract_number(filename):
    # Extract numeric part from filename
    match = re.search(r"_(\d+)", filename)
    if match:
        return int(match.group(1))
    else:
        return float("inf")  # Return infinity if no numeric part found


def generate_history(filename):
    global months_range
    print(f"started processing {filename}")

    with open(os.path.join(INPUT_DIR, filename), "r") as file:
        data = None
        try:
            data = json.load(file)
        except Exception as e:
            print(f"file: {filename} failed. {e}")
            return

    data["History"] = {}

    for month in months_range:
        month_str = month.strftime("%Y-%m-%d")
        try:
            data["performance_month"] = month_str
            response = requests.post(
                ENDPOINT_URL,
                json=data,
                allow_redirects=True,
            )

            if response.ok:
                response_data = response.json()
                data["History"][month_str] = {
                    "message_template": response_data["selected_candidate"][
                        "message_template_id"
                    ],
                    "message_generated_datetime": datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                    "measure": response_data["selected_candidate"]["measure"],
                    "acceptable_by": response_data["selected_candidate"][
                        "acceptable_by"
                    ],
                }
            else:
                if response.status_code != 400:
                    print(f"Error processing {filename}: code {response.status_code}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    name, extension = filename.split(".")
    new_filename = f"{name}_h.{extension}"
    with open(os.path.join(OUTPUT_DIR, new_filename), "w") as file:
        json.dump(data, file, indent=2)


def main():
    global months_range
    current_date = datetime.strptime(LATEST_HISTORY_MONTH, "%Y-%m-%d")

    for i in range(DURATION):
        m = current_date - relativedelta(months=i)
        months_range.append(m)

    months_range = months_range[::-1]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_files = sorted(
        [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")], key=extract_number
    )

    input_files = input_files[START:END]

    with ThreadPoolExecutor(WORKERS) as executor:
        executor.map(generate_history, input_files)


if __name__ == "__main__":
    main()
