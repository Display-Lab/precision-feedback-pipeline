import json
import os
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from google.auth.transport.requests import Request
from google.oauth2.service_account import IDTokenCredentials

# Define your OIDC Google Cloud service endpoint
ENDPOINT_URL = os.environ.setdefault(
    # "ENDPOINT_URL", "https://pfp.test.app.med.umich.edu/createprecisionfeedback"
    "ENDPOINT_URL",
    "http://localhost:8000/createprecisionfeedback/",
)

# Path to the directory containing input files
INPUT_DIR = os.environ.setdefault("INPUT_DIR", "")
WORKERS = int(os.environ.setdefault("WORKERS", "1"))
# Service account credentials (replace with your own)
SERVICE_ACCOUNT_KEY_PATH = os.environ.setdefault(
    "SERVICE_ACCOUNT_KEY_PATH", os.path.expanduser("~/service_account_key.json")
)
TARGET_AUDIENCE = os.environ.get("TARGET_AUDIENCE", None)
SAMPLE = int(os.getenv("SAMPLE", "0"))
START = int(os.getenv("START", "0"))
END = int(os.getenv("END", "10"))
OUTPUT = os.environ.get("OUTPUT", None)

process_candidates_str = os.environ.get("PROCESS_CANDIDATES", "True")
PROCESS_CANDIDATES = process_candidates_str.lower() in ["true", "t", "1", "yes"]
PERFORMANCE_MONTH = os.environ.get("PERFORMANCE_MONTH", None)

candidate_df: pd.DataFrame = pd.DataFrame()
response_df: pd.DataFrame = pd.DataFrame()
lock = threading.Lock()


def refresh_credentials(service_account_file, target_audience) -> IDTokenCredentials:
    # Usage:
    # service_account_file = 'path/to/service_account.json'
    # target_audience = 'https://service-you-are-calling.com'
    credentials = IDTokenCredentials.from_service_account_file(
        SERVICE_ACCOUNT_KEY_PATH, target_audience=TARGET_AUDIENCE
    )

    # Request a new token
    credentials.refresh(Request())

    return credentials


credential: IDTokenCredentials = (
    refresh_credentials(SERVICE_ACCOUNT_KEY_PATH, TARGET_AUDIENCE)
    if TARGET_AUDIENCE
    else None
)

count: int = 0


def post_json_message(filename):
    global credential
    try:
        with open(os.path.join(INPUT_DIR, filename), "r") as file:
            data = None
            try:
                data = json.load(file)
            except Exception as e:
                print(f"file: {filename} failed. {e}")
                return

            if PERFORMANCE_MONTH:
                data["performance_month"] = PERFORMANCE_MONTH
            
            headers = (
                {"Authorization": f"Bearer {credential.token}"} if credential else None
            )
            response = requests.post(
                ENDPOINT_URL,
                json=data,
                headers=headers,
                allow_redirects=True,
            )

            if response.status_code == 401:
                print(response.status_code)
                credential = refresh_credentials(
                    SERVICE_ACCOUNT_KEY_PATH, TARGET_AUDIENCE
                )
                response = requests.post(
                    ENDPOINT_URL,
                    json=data,
                    headers=headers,
                    allow_redirects=True,
                )

            if response.ok:
                response_data = response.json()
            elif response.status_code == 400:
                response_data = response.json()["detail"]

            with lock:
                add_response(response, response_data)
                if PROCESS_CANDIDATES:
                    add_candidates(response_data, data["performance_month"])

    except Exception as e:
        print(f"Error processing {filename}: {e}")


def add_candidates(response_data: dict, performance_month: str):
    global candidate_df
    data = response_data.get("candidates", None)
    if data:
        candidates = pd.DataFrame(data[1:], columns=data[0])
        candidates["performance_month"] = performance_month
        candidate_df = pd.concat([candidate_df, candidates], ignore_index=True)


def add_response(response: requests.Response, response_data):
    global response_df
    timing_total = response_data.get("timing", {}).get("total", float("NaN"))
    selected_candidate = response_data.get("selected_candidate", None)

    response_dict: dict = {
        "staff_number": [response_data.get("staff_number", None)],
        "causal_pathway": selected_candidate["acceptable_by"]
        if selected_candidate
        else [None],
        "status_code": [response.status_code],
        "elapsed": [response.elapsed.total_seconds()],
        "timing.total": [timing_total],
        "ok": [response.ok],
    }
    response_df = pd.concat(
        [response_df, pd.DataFrame(response_dict)], ignore_index=True
    )
    print(response_dict, end="\r")


def analyse_responses():
    global response_df
    r = (
        response_df.groupby("status_code")["elapsed"]
        .agg(count=("count"), response_time=("mean"))
        .reset_index()
    )

    r1 = (
        response_df.groupby("status_code")["timing.total"]
        .agg(pfp_time=("mean"))
        .reset_index()
    )

    r2 = (
        response_df.groupby("causal_pathway")["staff_number"]
        .agg(count=("count"))
        .reset_index()
    )

    r2["%  "] = round(r2["count"] / r2["count"].sum() * 100, 1)

    r = pd.merge(r, r1, on="status_code", how="left")

    r["pfp_time"] = round(r["pfp_time"] * 1000, 1)
    r["response_time"] = round(r["response_time"] * 1000, 1)

    print(f"\n {r} \n")

    print(f"\n {r2} \n")


def analyse_candidates():
    global candidate_df

    if OUTPUT:
        candidate_df.to_csv(OUTPUT, index=False)

    candidate_df.rename(columns={"acceptable_by": "causal_pathway"}, inplace=True)
    candidate_df["score"] = candidate_df["score"].astype(float)
    candidate_df.rename(columns={"name": "message"}, inplace=True)

    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.expand_frame_repr", False)
    # pd.set_option("display.width", 1000)
    # pd.set_option("display.max_colwidth", None)

    # causal pathways
    causal_pathway_report = build_table("causal_pathway")
    print(causal_pathway_report, "\n")

    # messages
    message_report = build_table("message")
    print(message_report, "\n")

    # measures
    measure_report = build_table("measure")
    print(measure_report, "\n")


def build_table(grouping_column):
    report_table = (
        candidate_df.groupby(grouping_column)["selected"]
        .agg(acceptable=("count"), selected=("sum"))
        .reset_index()
    )
    scores = round(
        candidate_df.groupby(grouping_column)["score"]
        .agg(acceptable_score=("mean"))
        .reset_index(),
        2,
    )
    report_table = pd.merge(report_table, scores, on=grouping_column, how="left")

    report_table["% acceptable"] = round(
        report_table["acceptable"] / report_table["acceptable"].sum() * 100, 1
    )
    report_table["% selected"] = round(
        report_table["selected"] / report_table["selected"].sum() * 100, 1
    )
    report_table["% of acceptable selected"] = round(
        report_table["selected"] / report_table["acceptable"] * 100, 1
    )
    selected_scores = round(
        candidate_df[candidate_df["selected"]]
        .groupby(grouping_column)["score"]
        .agg(selected_score=("mean"))
        .reset_index(),
        2,
    )
    report_table = pd.merge(
        report_table, selected_scores, on=grouping_column, how="left"
    )

    report_table = report_table[
        [
            grouping_column,
            "acceptable",
            "% acceptable",
            "acceptable_score",
            "selected",
            "% selected",
            "selected_score",
            "% of acceptable selected",
        ]
    ]

    return report_table


def extract_number(filename):
    # Extract numeric part from filename
    match = re.search(r"_(\d+)", filename)
    if match:
        return int(match.group(1))
    else:
        return float("inf")  # Return infinity if no numeric part found


def main():
    global count

    input_files = sorted(
        [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")], key=extract_number
    )

    input_files = input_files[START:END]

    if SAMPLE:
        n = min(SAMPLE, len(input_files))
        input_files = sorted(random.sample(input_files, n), key=extract_number)

    with ThreadPoolExecutor(WORKERS) as executor:
        executor.map(post_json_message, input_files)

    analyse_responses()
    if PROCESS_CANDIDATES:
        analyse_candidates()


if __name__ == "__main__":
    main()
