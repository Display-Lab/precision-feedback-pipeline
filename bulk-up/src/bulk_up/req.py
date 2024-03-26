import json
import os
from concurrent.futures import ThreadPoolExecutor
import time

import requests
from google.auth.transport.requests import Request
from google.oauth2.service_account import IDTokenCredentials

# Define your OIDC Google Cloud service endpoint
ENDPOINT_URL = os.environ.setdefault(
    "ENDPOINT_URL", "https://pfp.test.app.med.umich.edu/createprecisionfeedback"
)

# Path to the directory containing JSON files
JSON_DIR = "/Users/pboisver/dev/0221/ProviderInputMessages"
MAX_REQUESTS = int(os.environ.setdefault("MAX_REQUESTS", "10"))

# Service account credentials (replace with your own)
SERVICE_ACCOUNT_KEY_PATH = os.environ.setdefault(
    "SERVICE_ACCOUNT_KEY_PATH", os.path.expanduser("~/service_account_key.json")
)
TARGET_AUDIENCE = os.environ["TARGET_AUDIENCE"]


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

credential: IDTokenCredentials = refresh_credentials(
    SERVICE_ACCOUNT_KEY_PATH, TARGET_AUDIENCE
)


def post_json_message(filename):
    global credential

    # print(f"post with token: {credential.token}")
    try:
        with open(os.path.join(JSON_DIR, filename), "r") as file:
            data = json.load(file)
            print(
                f"\n{'Request':>10} {filename:>20}: message_instance_id = {data['message_instance_id']}"
            )
            response = requests.post(
                ENDPOINT_URL,
                json=data,
                headers={"Authorization": f"Bearer {credential.token}"},
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
                )

            response_data = response.json()

            message_instance_id = response_data.get("message_instance_id")
            print(
                f"{'Response:':>10} {filename:>20}: message_instance_id = {message_instance_id}, {response.status_code}"
            )
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")


def main():
    json_files = sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json")])

    # print(f"files: {json_files}")

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(post_json_message, json_files[0:MAX_REQUESTS])
        
    # for message in json_files[0:MAX_REQUESTS]:
    #     post_json_message(message)
    #     time.sleep(0)


if __name__ == "__main__":
    main()
