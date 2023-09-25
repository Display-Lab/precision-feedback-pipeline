# Because github doesn't have a good way to programmatically access the data from an entire folder,
# a workaround is to iterate through the entries in a folder and individually pull them all down.
# We can write the function then to pull 'raw' files and then can have it configured to either
# pull all of the directory when running normally, or with a restricted subset by an env var...

# With how the code currently works, it likes there to be a local file to read from, which I have
# no issues with since it works great currently. There may be some merit to changing things to 
# allow a direct reference to an external file when we are doing startup, but as a quick proof of 
# concept I will re-write them so everything gets saved locally and then referenced from there...
import os
import requests
import json


## Function to modularly fetch JSON content from GitHub
def get_git_json(branch, folder_path, file_name):
    # Construct raw github link:
    github_url = f"https://raw.githubusercontent.com/Display-Lab/knowledge-base/{branch}/{folder_path}/{file_name}.json"
    header = {"Accept": "application/vnd.github.v3.raw"} # Tell GitHub to send as raw, uncompressed version
    content = requests.get(github_url, headers=header)
    
    if content.status_code == 200:
        try:
            json_content = json.dumps(json.loads(content.text), indent=4) # Reconstruct as JSON with indentation
            return json_content
        except json.JSONDecodeError as e:
            raise Exception("Failed parsing JSON content.")
    else:
        raise Exception(f"Failed to fetch JSON content from GitHub link: {github_url}")



## Retrieve a github repo's contents and save them locally on startup:
def download_git_folder(folder):
    # Define the GitHub repository and folder path
    repo_url = f"https://api.github.com/repos/Display-Lab/knowledge-base/contents/{folder}"

    # Directory where we will save the downloaded files on startup:
    local_directory = os.path.dirname(f'startup/{folder}/')

    # Make a GET request to the GitHub API to list the contents of the folder
    response = requests.get(repo_url)

    if response.status_code == 200:
        # Parse the JSON response
        contents = response.json()

        # Ensure the local directory exists; create it if necessary
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        # Iterate through the contents, download files, and save them locally
        for item in contents:
            if item["type"] == "file":
                file_name = item["name"]
                file_content = requests.get(item["download_url"]).content
                local_file_path = os.path.join(local_directory, file_name)
                with open(local_file_path, "wb") as local_file:
                    local_file.write(file_content)
                    print(f"Downloaded: {file_name} to {local_file_path}")
    else:
        print(f"Failed to retrieve GitHub contents: {response.status_code}")



## Function to call when restricting the templates or pathways 'known' by the pipeline:
def set_knowledgebase_restrictions():
    global pathways, templates
    # Set causal pathway data for this startup of the pipeline:
    if os.environ.get("RESTRICTED_CP") != None:
        print(f'Restricting to causal pathway set by "RESTRICTED_CP"')
        # Retrieve only one causal pathway JSON file from github by user set env var (eg 'goal_gain')
        pathways = get_git_json('main', 'causal_pathways', os.environ.get('RESTRICTED_CP'))
    
    ## Set message template data for this startup of the pipeline:
    if os.environ.get("RESTRICTED_TEMPLATE") != None:
        print(f'Restricting to message template set by "RESTRICTED_TEMPLATE"')
        # Retrieve only one message template file from github by user set env var (eg 'in_top_25%')
        templates = get_git_json('main', 'message_templates', os.environ.get('RESTRICTED_TEMPLATE'))