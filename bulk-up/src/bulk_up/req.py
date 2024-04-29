import json
import os
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

# Path to the directory containing JSON files
JSON_DIR = "/home/faridsei/dev/test/ProviderInputMessages"
MAX_REQUESTS = int(os.environ.setdefault("MAX_REQUESTS", "10"))
WORKERS = int(os.environ.setdefault("WORKERS", "10"))
# Service account credentials (replace with your own)
SERVICE_ACCOUNT_KEY_PATH = os.environ.setdefault(
    "SERVICE_ACCOUNT_KEY_PATH", os.path.expanduser("~/service_account_key.json")
)
TARGET_AUDIENCE = os.environ.get("TARGET_AUDIENCE", None)
candidate_df: pd.DataFrame = pd.DataFrame()
response_df: pd.DataFrame = pd.DataFrame()
lock = threading.Lock()


def refresh_credentials(service_account_file, target_audience) -> IDTokenCredentials:
    # Load the service account credentials from the file
    credentials = IDTokenCredentials.from_service_account_file(
        SERVICE_ACCOUNT_KEY_PATH, target_audience=TARGET_AUDIENCE
    )

    # Request a new token
    credentials.refresh(Request())

    return credentials


# Usage:
# service_account_file = 'path/to/service_account.json'
# target_audience = 'https://service-you-are-calling.com'
# new_token = get_new_token(service_account_file, target_audience)

# Initialize credentials
# credentials = IDTokenCredentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH)
# credentials.refresh(Request())

credential: IDTokenCredentials = (
    refresh_credentials(SERVICE_ACCOUNT_KEY_PATH, TARGET_AUDIENCE)
    if TARGET_AUDIENCE
    else {"token": None}
)

count: int = 0


def post_json_message(filename):
    global credential

    # print(f"post with token: {credential.token}")
    try:
        with open(os.path.join(JSON_DIR, filename), "r") as file:
            data = json.load(file)

            response = requests.post(
                ENDPOINT_URL,
                json=data,
                headers={"Authorization": f"Bearer {credential['token']}"},
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
                    headers={"Authorization": f"Bearer {credential.token}"},
                    allow_redirects=True,
                )

            response_data = response.json()

            with lock:
                add_response(response, response_data)
                add_candidates(response_data)

    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")


def add_candidates(response_data: dict):
    global candidate_df
    data = response_data.get("candidates", None)
    if data:
        candidate_df = pd.concat(
            [candidate_df, pd.DataFrame(data[1:], columns=data[0])], ignore_index=True
        )


def add_response(response: requests.Response, response_data):
    global response_df
    timing_total = response_data.get("timing", {}).get("total", None)
    response_dict: dict = {
        "staff_number": [response_data.get("staff_number", None)],
        "status_code": [response.status_code],
        "elapsed": [response.elapsed.total_seconds()],
        "timing.total": [timing_total],
        "ok": [response.ok],
    }
    response_df = pd.concat(
        [response_df, pd.DataFrame(response_dict)], ignore_index=True
    )
    print(response_dict)


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

    r = pd.merge(r, r1, on="status_code")

    r["pfp_time"] = round(r["pfp_time"] * 1000, 1)
    r["response_time"] = round(r["response_time"] * 1000, 1)

    
    print(f"\n {r} \n")


def analyse_candidates():
    global candidate_df
    candidate_df.rename(columns={"acceptable_by": "causal_pathway"}, inplace=True)
    causal_pathway = (
        candidate_df.groupby("causal_pathway")["selected"]
        .agg(acceptable=("count"), selected=("sum"))
        .reset_index()
    )
    causal_pathway["%"] = round(
        causal_pathway["acceptable"] / causal_pathway["acceptable"].sum() * 100, 1
    )
    causal_pathway["selected %"] = round(
        causal_pathway["selected"] / causal_pathway["acceptable"] * 100, 1
    )

    causal_pathway = causal_pathway[
        ["causal_pathway", "%", "acceptable", "selected", "selected %"]
    ]
    print(causal_pathway, "\n")

    measure = (
        candidate_df.groupby("measure")["selected"]
        .agg(total=("count"), selected=("sum"))
        .reset_index()
    )
    measure["%"] = round(measure["total"] / measure["total"].sum() * 100, 1)
    measure["selected %"] = round(measure["selected"] / measure["total"] * 100, 1)

    measure = measure[["measure", "%", "total", "selected", "selected %"]]
    print(measure, "\n")
    
    candidate_df.rename(columns={"name": "message"}, inplace=True)
    message = (
        candidate_df.groupby("message")["selected"]
        .agg(total=("count"), selected=("sum"))
        .reset_index()
    )
    message["%"] = round(message["total"] / message["total"].sum() * 100, 1)
    message["selected %"] = round(message["selected"] / message["total"] * 100, 1)

    message = message[["message", "%", "total", "selected", "selected %"]]
    print(message, "\n")

    pass


def main():
    global count

    json_files = sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json")])

    # print(f"files: {json_files}")

    with ThreadPoolExecutor(WORKERS) as executor:
        executor.map(post_json_message, json_files[0:MAX_REQUESTS])

    # for message in json_files[0:MAX_REQUESTS]:
    #     post_json_message(message)
    #     time.sleep(0)
    analyse_responses()
    analyse_candidates()


if __name__ == "__main__":
    main()
