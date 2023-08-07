import pandas as pd
import json
import requests
import time
import os
import argparse
import base64
import certifi
import google.auth.transport.requests
import requests

from google.auth import crypt
from google.oauth2 import service_account
global iniRow,finRow,numCol,reqNumber,target,useGit,showResp,saveResp,perfPath,pfp,vers
vers = "1.1.2"

## Initialize argparse, define command-line arguments
parser = argparse.ArgumentParser(description="Leakdown Tester Script")
parser.add_argument("--respond", action="store_true", help="Logical flag to print API responses. Default = True; use '--respond' to see responses.")
parser.add_argument("--save", action="store_true", help="Logical flag to save API responses. Default = True; use '--save' to save outputs.")
parser.add_argument("--RI", type=int, default=0, help="First row of data to read from CSV.")
parser.add_argument("--RF", type=int, default=12, help="Last row of data to read from CSV.")
parser.add_argument("--C", type=int, default=10, help="Number of columns to read.")
parser.add_argument("--reqs", type=int, default=1, help="Number of post requests to send.")
parser.add_argument("--target", choices=["local", "heroku", "cloud"], default="local", help="Target PFP environment: use 'local', 'heroku', or 'cloud'.")
parser.add_argument("--useGit", type=str, default=None, help="Address of GitHub input message file to send pipeline.")
parser.add_argument("--csv", type=str, default=None, help="Filepath to CSV file to read from.")
parser.add_argument("--service_account", type=str, default=None, help="Filepath to the service account file to read from" )

## Parse command-line arguments and pull in environmental variables
args = parser.parse_args()
iniRow =    args.RI         # Initial row read from CSV
finRow =    args.RF         # Final row read from CSV
numCol =    args.C          # Number of columns read
reqNumber = args.reqs       # Number of Requests sent
target =    args.target     # Flag: API endpoint target
useGit =    args.useGit     # Flag: GitHub JSON source
showResp =  args.respond    # Flag: Print API response to console
saveResp =  args.save       # Flag: Save API response to file
csvPath =   args.csv        # CSV file path (argument specified)
serviceaccountPath = args.service_account #Service Account file path(argument specified)
perfPath =  os.environ.get("CSVPATH")
pfp =       os.environ.get("PFP")
target_audience = os.environ.get("TARGET_AUDIENCE")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Function to fetch JSON content from GitHub... V9
def go_fetch(url):
    if "github.com" in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob", "")
    header = {"Accept": "application/vnd.github.v3.raw"} # tell gitHub to send as raw, uncompressed
    bone = requests.get(url, headers=header)
    
    if bone.status_code == 200:
        try:
            jasonBone = json.dumps(json.loads(bone.text), indent=4) # reconstruct as JSON with indentation
            return jasonBone
        except json.JSONDecodeError as e:
            raise ValueError("Failed parsing JSON content.")
    else:
        raise ValueError(f"Failed to fetch JSON content from GitHub link: {url}")

# Reading in CSV data from file...
def csv_trans_json(path):
    performance = pd.read_csv(path, header=None, usecols = range(numCol), nrows= finRow-iniRow)
    rowsRead, colsRead = performance.shape
    selectedRows = performance.iloc[iniRow : finRow]
    jsonedData = ""
    
    # Integrated dimension error catcher:
    if colsRead != numCol or rowsRead != finRow - iniRow:
        raise ValueError(f"Read error; expected {finRow - iniRow} rows and {numCol} columns. Actual data is {rowsRead} rows by {colsRead} columns.")

    # Integrated Dataframe to JSON conversion (V.15)
    for i, row in selectedRows.iterrows():
        current_line = json.dumps(row.to_list())
        jsonedData += current_line  # content addition
        if i < len(performance) - 1:
            jsonedData += ",\n\t"   # formatting
    return jsonedData

# Create JSON Payload...
def assemble_payload(warhead):
    missile = '''{
      "@context": {
        "@vocab": "http://schema.org/",
        "slowmo": "http://example.com/slowmo#",
        "csvw": "http://www.w3.org/ns/csvw#",
        "dc": "http://purl.org/dc/terms/",
        "psdo": "http://purl.obolibrary.org/obo/",
        "slowmo:Measure": "http://example.com/slowmo#Measure",
        "slowmo:IsAboutPerformer": "http://example.com/slowmo#IsAboutPerformer",
        "slowmo:ColumnUse": "http://example.com/slowmo#ColumnUse",
        "slowmo:IsAboutTemplate": "http://example.com/slowmo#IsAboutTemplate",
        "slowmo:spek": "http://example.com/slowmo#spek",
        "slowmo:IsAboutCausalPathway": "http://example.com/slowmo#IsAboutCausalPathway",
        "slowmo:IsAboutOrganization": "http://example.com/slowmo#IsAboutOrganization",
        "slowmo:IsAboutMeasure": "http://example.com/slowmo#IsAboutMeasure",
        "slowmo:InputTable": "http://example.com/slowmo#InputTable",
        "slowmo:WithComparator": "http://example.com/slowmo#WithComparator",
        "has_part": "http://purl.obolibrary.org/obo/bfo#BFO_0000051",
        "has_disposition": "http://purl.obolibrary.org/obo/RO_0000091"
      },
      "Performance_data":[
        ["staff_number","measure","month","passed_count","flagged_count","denominator","peer_average_comparator","peer_90th_percentile_benchmark","peer_75th_percentile_benchmark","MPOG_goal"],
        '''
    missile += warhead
    missile += '''
        ],
        "History":{
            "Month1": 
              {
                "staff_number": 30,
                "selected_candidate": {
                   "message_template": "https://repo.metadatacenter.org/template-instances/33412958-7985-43c2-ba21-0c35b2b4ead1",
                    "has_disposition": ["positive gap content"],
                    "has_moderator": ["positive trend"],
                    "display": "line graph 12-month",
                    "measure": "SUS-04",
                    "acceptable_by": ["social gain", "social better"]
                    } ,
                "performance_month": "2023-03",
                "message_generated_datetime": "2023-04-23 12:02:03",
                "pfkb_version": "1.0.1",
                "pfp_version": "1.2.2",
                "email_text_html": "<p>Congratulations on your high performance for SUS-04: Fresh Gas Flow, less than or equal to 2L/min. Your performance was 96%, above the Top 10% peer benchmark of 94%.</p> <p>More details about how the measure SUS-04 is calculated <a href='[insert link here]'> are available here</a>. Details about your operative cases are available in your <a href='[insert link here]'> clinical quality dashboard</a>.</p>"
               }
        },
        "Preferences":{
          "Utilities": {
          "Message_Format": 
            {
              "1": "0.0",
              "2": "0.1",
              "16": "7.5",
              "24": "9.4",
              "18": "11.3",
              "11": "13.2",
              "22": "15.1" ,
              "14": "22.6" ,
              "21": "62.3" ,
              "5":"0.2",
              "15":"4.0",
              "4":"0.9"
            },
          "Display_Format":
            {
              "short_sentence_with_no_chart": "0.0",
              "bar": "37.0",
              "line": "0.0"
            }
        }
      },
      "debug":"no"
      }'''
    return missile

# Function to send the post request...
def send_req(pfp, missile):
	headers1 = {"Content-Type": "application/json"}
	response = requests.post(pfp, data=missile, headers=headers1)
	return response

# Output relevant JSON keys from API response...
def text_back(postReturn):
    if "selected_candidate" in postReturn:
        selCan = postReturn["selected_candidate"]
        print("Selected Candidate Message Information:")
        print(f"Display: {selCan.get('display')}")
        print(f"Measure: {selCan.get('measure')}")
        print(f"Acceptable By: {selCan.get('acceptable_by')}")

    if "Message" in postReturn:
        messDat = postReturn["Message"]
        print(f"Text Message: {messDat.get('text_message')}")
        print(f"Comparison Value: {messDat.get('comparison_value')}\n")

# Save PFP API responses for review...
def log_return(postReturn, outputName):
    texName = outputName + ".json"
    imgName = outputName + ".png"
    with open(texName, "w") as file:
        json.dump(postReturn, file, indent=2)
        print(f"PFP response text saved to '{texName}'")
    with open(imgName, "wb") as imageFile:
        imageFile.write(base64.b64decode(postReturn["Message"]["image"]))
        print(f"Pictoralist image saved to '{imgName}'.\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def make_iap_request(url,Fullmessage, method="POST", **kwargs):
    """Makes a request to an application protected by Identity-Aware Proxy.

    Args:
      url: The Identity-Aware Proxy-protected URL to fetch.
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.

    Returns:
      The page body, or raises an exception if the page couldn't be retrieved.
    """
    # Set the default timeout, if missing
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90

    # True if the credentials have a token and the token is not expired. This
    # obviates the need to track expiry times ourselves.
    if oidc_token.valid != True:
        
        request = google.auth.transport.requests.Request()
        oidc_token.refresh(request)

    # Fetch the Identity-Aware Proxy-protected URL, including an
    # Authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    Fullmessage=json.loads(Fullmessage)
    resp = requests.post(
       
        url,
        headers={"Authorization": "Bearer {}".format(oidc_token.token)},
        json=Fullmessage,
        
    )
    if resp.status_code == 403:
        raise Exception(
            "Service account does not have permission to "
            "access the IAP-protected application."
        )
    elif resp.status_code != 200:
        raise Exception(
            "Bad response from application: {!r} / {!r} / {!r}".format(
                resp.status_code, resp.headers, resp.text
            )
        )
    else:
        return resp

if __name__ == "__main__":
    print(f"\n\t\tWelcome to the Leakdown Tester, Version {vers}!")
    
    # Argument-set API endpoint logic
    if target == "local" and not pfp:
        pfp = "http://127.0.0.1:8000/createprecisionfeedback/"
    elif target == "heroku" and not pfp:
        pfp = "https://pfpapi.herokuapp.com/createprecisionfeedback/"
    elif target == "cloud" and not pfp:
        pfp = "https://pfp.test.app.med.umich.edu/createprecisionfeedback"
    else:
        print("Warning: Target not declared. Continuing with local PFP target.")

    # Argument-set CSV filepath (overrides Env Var)
    if csvPath != None:
        perfPath = csvPath
    
    oidc_token = service_account.IDTokenCredentials.from_service_account_file(
    serviceaccountPath,
    target_audience=target_audience,
)

    # Error handling - JSON content source
    if perfPath == None and useGit == None:
        raise ValueError("Please specify where to read JSON content from.")
    elif perfPath != None and useGit != None:
        print("\tINFO: JSON payloads specified by both GitHub link and filepath.")
        print("Continuing with GitHub payload...")

    # Startup config readback
    if useGit != None:
        print(f"Reading JSON data from {useGit}...")
    elif perfPath != None:
        if csvPath == None:
            print("Using CSV data specified by environmental variable...")
        print(f"Reading data from {perfPath}...")
        print(f"Reading in data with dimensions {numCol} by {finRow - iniRow}...")
    print(f"Sending {reqNumber} request(s) to {pfp}...\n")

    #### Main script function calls ####
    try:
        # GitHub JSON Payload implementation
        if useGit != None:
            fullMessage = go_fetch(useGit)    
        # Building JSON from CSV
        elif perfPath != None:
            perfJSON = csv_trans_json(perfPath)   # I/O from CSV dataframe
            fullMessage = assemble_payload(perfJSON)    # Make JSON payload
        else:
            print("Error: No content provided for POST request.")
            exit(1)

        for i in range(reqNumber):
            # Send the POST request(s) to the PFP
            print(f"Trying request {i + 1} of {reqNumber}:")
            airtime = time.time()
            if target == "heroku" and target == "local":
                sentPost = send_req(pfp, fullMessage)
            elif target == "cloud":
                sentPost = make_iap_request(pfp,fullMessage)
                print(sentPost)
            # Check response(s)
            if sentPost.status_code == 200:
                print("Message delivered in {:.3f} seconds.\n".format(time.time() - airtime))
                # Output response information (on request)
                if showResp:
                    print("\n\t\t The API has returned the following:")
                    apiReturn = json.loads(sentPost.text)    # response to JSON
                    text_back(apiReturn)

                # Save response data to files (on request)
                if saveResp:
                    respName = f"response_{i + 1}"
                    log_return(apiReturn, respName)

            else:
                print(f"Delivery failed. Returned status code {sentPost.status_code}.")

        print("\t\tLeakdown Test complete.\n")

    except ValueError as e:
        print(f"Error: {e}")