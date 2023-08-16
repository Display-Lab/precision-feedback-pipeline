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
from LDT_Addendum import vignAccPairs, payloadHeader, payloadFooter
from google.auth import crypt
from google.oauth2 import service_account

global iniRow,finRow,numCol,reqNumber,target,useGit,showResp,saveResp,perfPath,pfp,audience,vers,chkPairs
vers = "1.4.2"

## Initialize argparse, define command-line arguments
ap = argparse.ArgumentParser(description="Leakdown Tester Script")
# Integer Args
ap.add_argument("--RI", type=int, default=0, help="First row of data to read from CSV.")
ap.add_argument("--RF", type=int, default=12, help="Last row of data to read from CSV.")
ap.add_argument("--C", type=int, default=10, help="Number of columns to read.")
ap.add_argument("--reqs", type=int, default=1, help="Number of post requests to send.")
# String Args
ap.add_argument("--target", choices=["local", "heroku", "cloud"], default="local", help="Target PFP environment: use 'local', 'heroku', or 'cloud'.")
ap.add_argument("--useGit", type=str, default=None, help="Address of GitHub input message file to send pipeline.")
ap.add_argument("--persona", choices=["alice", "bob", "chikondi", "deepa", "eugene", "fahad", "gaile"], help="Select a persona for testing.")
ap.add_argument("--csv", type=str, default=None, help="Filepath to CSV file to read from.")
ap.add_argument("--servAcc", type=str, default=None, help="Filepath to the service account file to read from" )
# Logical Args
ap.add_argument("--respond", action="store_true", help="Logical flag to print API responses. Default = True; use '--respond' to see responses.")
ap.add_argument("--save", action="store_true", help="Logical flag to save API responses. Default = True; use '--save' to save outputs.")
ap.add_argument("--repoTest", action="store_true", help="Logical flag to test knowledgebase repo files.")
ap.add_argument("--validate", action="store_true", help="Logical flag to check output message against known good data library.")

## Assign Environmental Variables
pfp =           os.environ.get("PFP")
audience =      os.environ.get("TARGET_AUDIENCE")

## Parse command-line arguments, use Env Vars if Args not used
args = ap.parse_args()
perfPath =    args.csv      if args.csv != None else os.environ.get("CSVPATH")      # Path to performance CSV data
servAccPath = args.servAcc  if args.servAcc != None else os.environ.get("SAPATH")   # Path to service account file

iniRow =    args.RI         # Initial row read from CSV
finRow =    args.RF         # Final row read from CSV
numCol =    args.C          # Number of columns read
reqNumber = args.reqs       # Number of Requests sent
target =    args.target     # API endpoint target
useGit =    args.useGit     # GitHub JSON source
usePers =   args.persona    # Use GitHub single persona to test alone
showResp =  args.respond    # Prints API response(s) to console
saveResp =  args.save       # Saves API response(s) to file
repoTest =  args.repoTest   # Tests knowledgebase repo files
chkPairs =  args.validate   # Checks output message(s) against vignette data

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#### Startup Functions ########################################################

## Configure API endpoint from argument...
def set_target():
    global pfp, oidcToken
    
    # Local API target:
    if target == "local":
        pfp = "http://127.0.0.1:8000/createprecisionfeedback/"
    
    # Heroku API target:
    elif target == "heroku":
        pfp = "https://pfpapi.herokuapp.com/createprecisionfeedback/"
    
    # GCP API target (ft. token retrieval):
    elif target == "cloud":
        assert audience, "Target Audience not set. Exiting..."
        assert servAccPath, "Service Account Path not set. Exiting..."

        pfp = "https://pfp.test.app.med.umich.edu/createprecisionfeedback/"
        oidcToken = service_account.IDTokenCredentials.from_service_account_file(
        servAccPath,
        target_audience = audience,
        )
    
    else:
        print("Warning: Target not declared. Continuing with local PFP target.")


## Handle JSON content pathing (& errors)...
def confirm_content():
    global perfPath
    assert perfPath != None or useGit != None, "No JSON content specified. Exiting..."
    
    if perfPath != None and useGit != None:
        print("\tINFO: Multiple JSON payloads specified.")
        print("\tContinuing with GitHub payload...")


## Startup configuration setting readback...
def startup_checklist():
    if useGit != None:
        print(f"Reading JSON data from {useGit}...")
    
    elif repoTest or usePers:
            print("Running automated input_message test(s)...")
    else:
        print(f"Reading data from {perfPath}...")
        print(f"Reading in data with dimensions {numCol} by {finRow - iniRow}...")
    
    print(f"Sending POST request(s) to {pfp}...\n")

#### Print Statements and Response Handling ################################

## Print relevant JSON keys from API response...
def text_back(postReturn):
    assert "staff_number" in postReturn, "Key 'staff_number' not found in post response."
    assert "selected_candidate" in postReturn, "Key 'selected_candidate' not found in post response."
    assert "Message" in postReturn, "Key 'Message' not found in post response." 
    
    selCan = postReturn["selected_candidate"]
    messDat = postReturn["Message"]
    print("\nAPI response contains keys:")
    print(f"Staff ID Number:\t{postReturn['staff_number']}")
    print(f"Display Type:\t\t{selCan.get('display')}")
    print(f"Measure:\t\t{selCan.get('measure')}")
    print(f"Acceptable By:\t\t{selCan.get('acceptable_by')}")
    print(f"Abbreviated Message:\t{messDat.get('text_message')[:50]}")
    print(f"Comparison Value:\t{messDat.get('comparison_value')}\n")


## Check output message for known-good metadata pairs...
def validate_output(apiReturn, staffID):
    match = False
    validKeys = vignAccPairs.get(staffID)
    chosenKeys = {
        "acceptable_by": apiReturn["selected_candidate"].get("acceptable_by").lower(),
        "measure": apiReturn["selected_candidate"].get("measure")
    }
    
    # Iterate through validation dict, check for matches
    for n in validKeys:
        if n == chosenKeys:
            match = True
            break
    if match:
        print(f"VIGNETTE VALIDATION:\tPASS\n\tOutput matches vignette expectations.")
    else:
        print("VIGNETTE VALIDATION:\tFAIL\n\tUnexpected message content.")
    #assert match, f"INFO:\tOutput message is not vignette consistent for {persona}"


## Save PFP API responses for manual review...
def log_return(postReturn, outputName):
    texName = outputName + ".json"
    imgName = outputName + ".png"
    
    with open(texName, "w") as file:
        json.dump(postReturn, file, indent=2)
        print(f"PFP response text saved to '{texName}'")
    
    with open(imgName, "wb") as imageFile:
        imageFile.write(base64.b64decode(postReturn["Message"]["image"]))
        print(f"Pictoralist image saved to '{imgName}'.\n\n")


## Handle API responses...
def handle_response(response, requestNumber, staffID):
    if response.status_code == 200:
        print("Message delivered in {:.3f} seconds.".format(response.elapsed.total_seconds()))
        apiReturn = json.loads(response.text)
        
        if showResp:    # Print output if asked
            text_back(apiReturn)

        if chkPairs:    # Validate output if asked
            validate_output(apiReturn, staffID)
            
        if saveResp:    # Save output if asked
            respName = f"response_{requestNumber}"
            log_return(apiReturn, respName)

    else:
        if target == "cloud":
            raise Exception("Bad response from target API:\nStatus Code:\t{!r}\nHeaders: {!r}\n{!r}".format(
            response.status_code, response.headers, response.text))
        
        else:
            raise Exception("Bad response from target API:\nStatus Code:\t{!r}\n{!r}\n".format(
            response.status_code, response.text))


##### JSON Content Functions ########################################

## Fetch JSON content from GitHub... (V9)
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
            raise Exception("Failed parsing JSON content.")
    else:
        raise Exception(f"Failed to fetch JSON content from GitHub link: {url}")


## Read in CSV data from file, convert to JSON...
def csv_jsoner(path):
    performance = pd.read_csv(path, header=None, usecols = range(numCol), nrows= finRow-iniRow)
    rowsRead, colsRead = performance.shape
    selectedRows = performance.iloc[iniRow : finRow]
    jsonedData = ""
    
    # Integrated dimension error catcher:
    if colsRead != numCol or rowsRead != finRow - iniRow:
        raise ValueError(f"Expected {finRow - iniRow} rows and {numCol} columns. Actual data is {rowsRead} rows by {colsRead} columns.")

    # Integrated Dataframe to JSON conversion (V.15)
    for i, row in selectedRows.iterrows():
        currentLine = json.dumps(row.to_list())
        jsonedData += currentLine  # content addition
        if i < len(performance) - 1:
            jsonedData += ",\n\t"   # formatting
    return jsonedData


#### POST Functions ##################################################

## Send POST request to unprotected URLs...
def send_req(pfp, missile):
	header = {"Content-Type": "application/json"}
	response = requests.post(pfp, data=missile, headers=header)
	return response


## Send POST to IAP protected URLs...
def make_iap_request(url, Fullmessage, method="POST", **kwargs):

    # Set the default timeout, if missing
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90

    # Check if token valid, refresh expired token if not
    if oidcToken.valid != True:
        request = google.auth.transport.requests.Request()
        oidcToken.refresh(request)

    # Fetch the Identity-Aware Proxy-protected URL, including an
    # Authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    Fullmessage=json.loads(Fullmessage)
    resp = requests.post(
        url,
        headers={"Authorization": "Bearer {}".format(oidcToken.token)},
        json=Fullmessage,
    )
    return resp

## Test a knowledgebase repo input_message.json file...
def test_persona(persona, requestNumber, sigmaReqs):
    url = f"https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/vignettes/personas/{persona}/input_message.json"
    
    try:
        print(f"\t\nTrying request {requestNumber} of {sigmaReqs}: Persona '{persona.upper()}'")
        jsonContent = go_fetch(url)
        response = send_req(pfp, jsonContent)
        assert response.headers.get('content-type') == 'application/json', f"Bad response - Non-JSON content returned"
        respJson = response.json()
        handle_response(response, requestNumber, respJson["staff_number"])

    except AssertionError as ae:
        print(ae)
        #print(f"Continuing with test...\n")
        #continue

    except Exception as e:
        print(f"{e}")

## Automated full repo testing of all knowledgebase files...
def repo_test():
    hitlist = ["alice", "bob", "chikondi", "deepa", "eugene", "fahad", "gaile"]
    for requestNumber, persona in enumerate(hitlist, start=1):
        test_persona(persona, requestNumber, len(hitlist))
    print("\nFinished automated full-repo test.\n")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

########### Main Script Body ################################
if __name__ == "__main__":
    print(f"\n\t\tWelcome to the Leakdown Tester, Version {vers}!")
    set_target()
    confirm_content()
    startup_checklist()

    try:
        # Call single persona repo test
        if usePers is not None:
            test_persona(usePers, 1, reqNumber)
            print("\n\t\tLeakdown test complete.\n")
            exit(0)

        # Call repo_test if requested
        if repoTest:
            repo_test()
            print("\n\t\tLeakdown test complete.\n")
            exit(0)

        # Retrieve GitHub JSON Payload if requested
        if useGit is not None:
            fullMessage = go_fetch(useGit)    
        
        # Build JSON from CSV (default/by request)
        elif perfPath != None:
            perfJSON = csv_jsoner(perfPath)             # I/O from CSV dataframe
            fullMessage = payloadHeader + perfJSON + payloadFooter    # Make JSON payload
        
        else:
            print("Error: No content provided for POST request.")
            exit(1)

        # Send POST request(s)
        for i in range(reqNumber):
            print(f"Trying request {i + 1} of {reqNumber}:")
            
            if target == "heroku" or target == "local":
                sentPost = send_req(pfp, fullMessage)
                postJson = sentPost.json()
                handle_response(sentPost, i+1, postJson["staff_number"])
            
            elif target == "cloud":
                sentPost = make_iap_request(pfp, fullMessage)
                postJson = sentPost.json()
                handle_response(sentPost, i+1, postJson["staff_number"])
                print(sentPost)
        
        print("\t\tLeakdown test complete.\n")
        exit(0)

    except ValueError as e:
        print(f"{e}")
        exit(1)