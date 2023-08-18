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

global iniRow,finRow,numCol,numTests,target,useGit,showResp,saveResp,perfPath,pfp,audience,vers,chkPairs
vers = "1.4.3 (indev)"

## Initialize argparse, define command-line arguments
ap = argparse.ArgumentParser(description="Leakdown Tester Script")
# Integer Args
ap.add_argument("--RI", type=int, default=0, help="First row of data to read from CSV.")
ap.add_argument("--RF", type=int, default=12, help="Last row of data to read from CSV.")
ap.add_argument("--C", type=int, default=10, help="Number of columns to read.")
ap.add_argument("--tests", type=int, default=1, help="Number of Leakdown Tests to perform.")
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

iniRow =     args.RI         # Initial row read from CSV
finRow =     args.RF         # Final row read from CSV
numCol =     args.C          # Number of columns read
numTests =   args.tests      # Number of tests to perform
target =     args.target     # API endpoint target
useGit =     args.useGit     # GitHub JSON source
usePers =    args.persona    # Use GitHub single persona to test alone
showResp =   args.respond    # Prints API response(s) to console
saveResp =   args.save       # Saves API response(s) to file
repoTest =   args.repoTest   # Tests knowledgebase repo files
chkPairs =   args.validate   # Checks output message(s) against vignette data

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

##### Startup Functions #######################################################
### Handle API endpoint, script behavior, and number of requests to send.
### V 1.4.3+ has integrated readback as configurations are set.

## Set script behavior for JSON content source (+ error handling and readback)...
def set_behavior():
    global perfPath
    
    # Error catcher for multiple JSON payload specification
    if perfPath != None and useGit != None:
        print("INFO: Multiple JSON payloads specified.\n\tContinuing with GitHub payload...\n")
    
    # Set behavior to use GitHub content (1st priority)
    if useGit != None:      
        print(f"Reading JSON data from GitHub file at {useGit}...")
        return "github"
    
    # Set behavior to run single persona test
    elif usePers != None:
        print("Reading single input_message file from knowledgebase branch 'Main'...")
        return "oneRepo"
    
    # Set behavior to run full-repo tests
    elif repoTest:          
        print("Reading all input_message.json files from knowledgebase branch 'Main'...")
        return "fullRepo"
    
    # Set behavior to use CSV content (last priority)
    elif perfPath != None:
        print(f"Reading data from CSV file at '{perfPath}'...")
        print(f"Reading in data with dimensions {numCol} by {finRow - iniRow}...")
        return "CSV"
    
    else:
        print("Error: Behavior could not be set. No content specified for POST request.")
        exit(1)


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
    
    # Readback endpoint target when successfull
    print(f"Sending POST request(s) to API at '{pfp}'...")


## Calculate total number of POST requests script will try to send...
def calc_total_reqs(behavior, numberOfTests):
    if behavior == "fullRepo":
        totalRequests = numberOfTests * 7
    else:
        totalRequests = numberOfTests
    print(f"Sending a total of {totalRequests} POST requests...\n")
    return totalRequests


#### API Response Handling #########################################################

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
def response_vign_validate(apiReturn, staffID):
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
def handle_response(response, requestNumber):
    if response.status_code == 200:
        print("Response recieved in {:.3f} seconds.".format(response.elapsed.total_seconds()))
        apiReturn = json.loads(response.text)
        staffID = apiReturn["staff_number"]
        
        if showResp:    # Print output if asked
            text_back(apiReturn)

        if chkPairs:    # Validate output if asked
            response_vign_validate(apiReturn, staffID)
            
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


## Send POST request to IAP protected URLs...
def send_iap_req(url, Fullmessage, method="POST", **kwargs):

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
def test_persona(persona, requestNumber):
    url = f"https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/vignettes/personas/{persona}/input_message.json"
    
    try:
        print(f"\nTesting input_message file for persona '{persona.upper()}'")
        jsonContent = go_fetch(url)     # retrieve github json content
        
        if target != "cloud":
            response = send_req(pfp, jsonContent)   # send unprotected POST
    
        else:
            response = send_iap_req(pfp, jsonContent) # send protected POST

        handle_response(response, requestNumber)

    except Exception as e:
        print(f"{e}")

## Automated full repo testing of all knowledgebase files...
def repo_test():
    hitlist = ["alice", "bob", "chikondi", "deepa", "eugene", "fahad", "gaile"]
    for requestNumber, persona in enumerate(hitlist, start=1):
        test_persona(persona, requestNumber)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

########### Main Script Body ################################
def main():
    print(f"\n\t\tWelcome to the Leakdown Tester, Version {vers}!")
    try:
        behavior = set_behavior()   #Set script behavior, readback content source
        set_target()    #Set API endpoint, readback target
        sigmaReqs = calc_total_reqs(behavior, numTests)

        # Retrieve GitHub JSON Payload if requested
        if behavior == "github":
            fullMessage = go_fetch(useGit)    
        
        # Build JSON from CSV (default/by request)
        elif behavior == "CSV":
            perfJSON = csv_jsoner(perfPath)     # I/O from CSV dataframe
            fullMessage = payloadHeader + perfJSON + payloadFooter    # Make JSON payload


        # Send POST request(s)
        for i in range(numTests):
            print(f"\nRunning test {i+1} of {numTests}:")
            
            # Send single-persona repo test
            if behavior == "oneRepo":
                test_persona(usePers, i+1)
            
            # Send full-repo persona tests
            elif behavior == "fullRepo":
                repo_test()
            
            # Send POST requests for GitHub or CSV content types
            else:
                if target != "cloud":
                    sentPost = send_req(pfp, fullMessage)
                    postJson = sentPost.json()
                    handle_response(sentPost, i+1)
            
                elif target == "cloud":
                    sentPost = send_iap_req(pfp, fullMessage)
                    postJson = sentPost.json()
                    handle_response(sentPost, i+1)
        
        print("\n\t\tLeakdown test complete.\n")
        exit(0)


    except ValueError as e:
        print(f"{e}")
        exit(1)


if __name__ == "__main__":
    main()