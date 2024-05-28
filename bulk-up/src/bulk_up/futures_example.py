import concurrent
import json
import os
from concurrent.futures import ThreadPoolExecutor

import requests

# Directory containing JSON files
directory = "path/to/json_files"

# Web endpoint to post the JSON messages
web_endpoint = "http://example.com/post"


# Function to post a single JSON message
def post_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    response = requests.post(web_endpoint, json=data)
    return response.json()


# Function to process the responses and count causal_pathway
def process_responses(responses):
    causal_pathway_count = {}
    for response in responses:
        causal_pathway = response.get("causal_pathway")
        if causal_pathway:
            causal_pathway_count[causal_pathway] = (
                causal_pathway_count.get(causal_pathway, 0) + 1
            )
    return causal_pathway_count


# Main function to load JSON files and use a pool of threads to post them
def main():
    # Get a list of JSON files in the directory
    json_files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".json")
    ]

    # Use a ThreadPoolExecutor to post the JSON messages concurrently
    with ThreadPoolExecutor(max_workers=1) as executor:
        # Map post_json function to all JSON files
        future_to_json = {
            executor.submit(post_json, file_path): file_path for file_path in json_files
        }

        # Collect the responses as they complete
        responses = [
            future.result()
            for future in concurrent.futures.as_completed(future_to_json)
        ]

    # Process the responses to count causal_pathway
    causal_pathway_count = process_responses(responses)
    print(causal_pathway_count)


if __name__ == "__main__":
    main()
