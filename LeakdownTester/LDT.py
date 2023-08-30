import pandas as pd
import json
import requests
import time
import os
import argparse
import base64
import certifi
import google.auth.transport.requests
import threading
from google.auth import crypt
from google.oauth2 import service_account
from threading import Barrier
from LDT_Addendum import vignAccPairs, payloadHeader, payloadFooter, ldtVersion, hitlistCP, hitlistIM

global iniRow,finRow,numCol,numTests,target,useGit,showResp,saveResp,perfPath,pfp,audience,vers,chkPairs,numThreads,useCP

## Initialize argparse, define command-line arguments
ap = argparse.ArgumentParser(description="Leakdown Tester Script")
# Integer Args
ap.add_argument("--RI", type=int, default=0, help="First row of data to read from CSV.")
ap.add_argument("--RF", type=int, default=12, help="Last row of data to read from CSV.")
ap.add_argument("--C", type=int, default=10, help="Number of columns to read.")
ap.add_argument("--tests", type=int, default=1, help="Number of Leakdown Tests to perform.")
ap.add_argument("--threads", type=int, default=1, help="Number of threads to run Leakdown Tests on concurrently.")
# String Args
ap.add_argument("--target", choices=["local", "heroku", "cloud"], default="local", help="Target PFP environment: use 'local', 'heroku', or 'cloud'.")
ap.add_argument("--useGit", type=str, default=None, help="Address of GitHub input message file to send pipeline.")
ap.add_argument("--persona", choices=["alice", "bob", "chikondi", "deepa", "eugene", "fahad", "gaile"], help="Select a persona for testing.")
ap.add_argument("--pathway", choices=["goal_approach","goal_gain","goal_loss","improving","social_approach","social_better","social_gain","social_loss","social_worse","worsening"], help="Select a causal pathway (acronym) for testing.")
ap.add_argument("--csv", type=str, default=None, help="Filepath to CSV file to read from.")
ap.add_argument("--servAcc", type=str, default=None, help="Filepath to the service account file to read from" )
# Logical Args
ap.add_argument("--respond", action="store_true", help="Logical flag to print API responses. Default = True; use '--respond' to see responses.")
ap.add_argument("--save", action="store_true", help="Logical flag to save API responses. Default = True; use '--save' to save outputs.")
ap.add_argument("--allPersonas", action="store_true", help="Logical flag to test all knowledgebase persona input message files.")
ap.add_argument("--allCPs", action="store_true", help="Logical flag to test all causal-pathway-specific input message files.")
ap.add_argument("--vignVal", action="store_true", help="Logical flag to check output message against known good data library.")
ap.add_argument("--cpVal", action="store_true", help="Logical flag to compare input and output causal pathway for match.")

## Assign Environmental Variables
pfp =           os.environ.get("PFP")
audience =      os.environ.get("TARGET_AUDIENCE")

## Parse command-line arguments, use Env Vars if Args not used
args = ap.parse_args()
perfPath =    args.csv      if args.csv != None else os.environ.get("CSVPATH")      # Path to performance CSV data
servAccPath = args.servAcc  if args.servAcc != None else os.environ.get("SAPATH")   # Path to service account file
chkCP = args.cpVal          if args.pathway != None or args.allCPs else None        # Only allow CP check if testing CPs

iniRow =     args.RI            # Initial row read from CSV
finRow =     args.RF            # Final row read from CSV
numCol =     args.C             # Number of columns read
numTests =   args.tests         # Number of tests to perform
numThreads = args.threads       # Number of threads to test with concurrently
target =     args.target        # API endpoint target
useGit =     args.useGit        # GitHub JSON source
usePers =    args.persona       # Use GitHub single persona to test alone
useCP =      args.pathway       # Stores requested CP, tests one causal-pathway-specific input message
showResp =   args.respond       # Prints API response(s) to console
saveResp =   args.save          # Saves API response(s) to file
allPers =    args.allPersonas   # Tests all knowledgebase persona input message files
allCPs =     args.allCPs        # Tests all knowledgebase causal pathway input message files
chkPairs =   args.vignVal       # Checks output message(s) against vignette data

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
    
    # Set behavior to use user-specified GitHub content (1st priority)
    elif useGit != None:      
        print(f"Reading JSON data from GitHub file at {useGit}...")
        return "customGithub"
    
    # Set behavior to run single persona test (2nd)
    elif usePers != None:
        print("Reading single persona input_message file from knowledge-base 'Personas' folder...")
        return "onePers"
    
    # Set behavior to run all persona tests (3rd)
    elif allPers:          
        print("Reading all input_message.json files from knowledge-base 'Personas' folder...")
        return "allPers"

   # Set behavior to run single causal pathway test (4th)
    elif useCP !=  None:          
        print("Reading one JSON file from knowledge-base folder 'Causal Pathway Test Suite'...")
        return "oneCP"

   # Set behavior to run all causal pathway tests (5th)
    elif allCPs:          
        print("Reading all JSON files from knowledge-base folder 'Causal Pathway Test Suite'...")
        return "allCPs"

    # Set behavior to use CSV content (last priority)
    elif perfPath != None:
        print(f"Reading data from CSV file at '{perfPath}'...")
        print(f"Reading in data with dimensions {numCol} by {finRow - iniRow}...")
        return "CSV"
    
    else:
        print("Error occured setting Behavior: No content specified for POST request.")
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
    print(f"Sending POST request(s) to API at '{pfp}'...\n")



## Calculate total number of POST requests script will try to send...
def calc_total_reqs(behavior):
    if behavior == "allPers":
        totalRequests = len(hitlistIM) * numTests * numThreads
    if behavior == "allCPs":
        totalRequests = len(hitlistCP) * numTests * numThreads
    else:
        totalRequests = numTests * numThreads
    
    print(f"Sending {totalRequests} total POST requests...")
    return totalRequests


#### API Response Handling #########################################################
### These functions print out response output, handle making logs of response output,
### and validate responses against known-good data (vignette specifications)

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
    print(f"Abbreviated Message:\t{messDat.get('text_message')[:85]}")
    print(f"Comparison Value:\t{messDat.get('comparison_value')}\n")



## Check output message for known-good metadata pairs...
def response_vign_validate(apiReturn, staffID):
    validKeys = vignAccPairs.get(staffID)
    chosenKeys = {
        "acceptable_by": apiReturn["selected_candidate"].get("acceptable_by").lower(),
        "measure": apiReturn["selected_candidate"].get("measure")
    }
    
    # Make validKeys into a more readable format for printing
    formattedValidKeys = [f"\t{item['acceptable_by'].title()}\t\t{item['measure']}" for item in validKeys]
    
    # Check keys and print results
    if chosenKeys in validKeys:
        print(f"\nVIGNETTE VALIDATION:\tPASS\nValid pairs:")
        for formattedValidKey in formattedValidKeys:
            print(formattedValidKey)
        print(f"\nAPI returned pair:\n\t{chosenKeys['acceptable_by'].title()}\t\t{chosenKeys['measure']}\n")
    else:
        print(f"\nVIGNETTE VALIDATION:\tFAIL\nExpected valid pairs:")
        for formattedValidKey in formattedValidKeys:
            print(formattedValidKey)
        print(f"\nAPI returned pair:\n\t{chosenKeys['acceptable_by'].title()}\t\t{chosenKeys['measure']}\n")




## Check output message against requested Causal Pathway...
def response_CP_validate(apiReturn, causalPathway):
    assert causalPathway != None, ("Causal Pathway passed to validation function is not a string")
    causalPathway = causalPathway.replace("_"," ")      # replace underscores of user input with spaces
    selectedCP = apiReturn["selected_candidate"].get("acceptable_by").lower()
    
    # Check for match between selected causal pathway and specified causal pathway
    if causalPathway == selectedCP:
        print(f"\nCAUSAL PATHWAY VALIDATION:\tPASS\nSpecified Pathway:\t{causalPathway}\nAccepted Pathway:\t{selectedCP}\n")
    else:
        print(f"\nCAUSAL PATHWAY VALIDATION:\tFAIL\nSpecified Pathway:\t{causalPathway}\nAccepted Pathway:\t{selectedCP}\n")



## Save PFP API responses for manual review...
def log_return(postReturn, requestID):
    folderName = "Response Log"
    os.makedirs(folderName, exist_ok=True)

    texName = os.path.join(folderName, f"response_{requestID.lower()}.json")
    imgName = os.path.join(folderName, f"response_{requestID.lower()}.png")
    responseJson = postReturn.json()

    with open(texName, "w") as file:
        json.dump(responseJson, file, indent=2)
        print(f"PFP response text saved to '{texName}'")
    
    with open(imgName, "wb") as imageFile:
        imageFile.write(base64.b64decode(responseJson["Message"]["image"]))
        print(f"Pictoralist image saved to '{imgName}'.\n\n")



## Handle API responses (print resp, check response keys, save logs)...
def handle_response(response, requestID):
    if response.status_code == 200:
        print(f"{requestID}:\n    Response recieved in {response.elapsed.total_seconds():.3f} seconds.")

        apiReturn = response.json()
        staffID = apiReturn["staff_number"]
        
        if showResp:    # Print output if asked
            text_back(apiReturn)

        if chkPairs:    # Validate vignette measure/causal pathway pair in output if asked
            response_vign_validate(apiReturn, staffID)

        if chkCP:       # Validate causal pathway output if asked
            response_CP_validate(apiReturn, useCP)
            # not an ideal way to incorporate which causal pathway we want to assert, but workable
            
        if saveResp:    # Save output if asked
            log_return(response, requestID)

    else:
        raise Exception("Bad response from target API:\nStatus Code:\t{!r}\nHeaders: {!r}\n{!r}".format(
        response.status_code, response.headers, response.text))



##### JSON Content Functions ###########################################################
### These functions handle where and how to read in JSON content to make valid post
### requests to the API.

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


#### POST Functions ###################################################################
### Any and all functions that send a post request live here. Protected or unprotected,
### from any content source, and against any of the available API endpoints.


## Send POST request to unprotected URLs...
def send_unprotected_post(pfp, fullMessage):
    header = {"Content-Type": "application/json"}
    response = requests.post(pfp, data=fullMessage, headers=header)
    return response



## Send POST request to IAP protected URLs...
def send_iap_post(url, fullMessage, method="POST", **kwargs):

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
    fullMessage=json.loads(fullMessage)
    resp = requests.post(
        url,
        headers={"Authorization": "Bearer {}".format(oidcToken.token)},
        json=fullMessage,
    )
    return resp



## Send POST request (IAP or Unprotected), then handle response...
def post_and_respond(fullMessage, requestID):
    global pfp
    try:
        if target != "cloud":
            sentPost = send_unprotected_post(pfp, fullMessage)

        elif target == "cloud":
            sentPost = send_iap_post(pfp, fullMessage)
        
        handle_response(sentPost, requestID)
    
    except Exception as e:
        print(f"{e}")



## Test a knowledgebase repo input message JSON file...
def test_inputfile(mode, inputID, requestID):
    try:
        if mode == "testIMs":   # Check if testing official persona input messages
            url = f"https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/vignettes/personas/{inputID}/input_message.json"
            print(f"\nTesting input_message file for persona '{inputID.upper()}'")

        elif mode == "testCPs": # Check if testing causal pathway suite input messages
            url = f"https://github.com/Display-Lab/knowledge-base/blob/main/vignettes/dev_templates/causal_pathway_test_suite/{inputID}_cptest.json"
            inputID = inputID.replace("_"," ")  # replace underscores with spaces
            print(f"\nTesting input_message file for causal pathway '{inputID.upper()}'")
        
        jsonContent = go_fetch(url)     # retrieve github json content
        post_and_respond(jsonContent, requestID)

    except Exception as e:
        print(f"{e}")



## Automated full repo testing of all knowledgebase files...
def repo_test(mode, threadIndex, testIndex, requestID):
    global useCP
    if mode == "testIMs":   # Run when testing persona input messages
        hitlist = hitlistIM
    elif mode == "testCPs": # Run when testing causal pathway input messages
        hitlist = hitlistCP
    
    for requestIndex, inputID in enumerate(hitlist, start=1):
        requestID = f"Thread {threadIndex}, Test {testIndex}, Request {requestIndex}" # add request index to ID
        useCP = inputID     # Sneaky way to set current causal pathway from hitlist for validation
        test_inputfile(mode, inputID, requestID)



## Run POST requests while tracking thread number...
## Handles logic previously assigned to main script body
def run_requests(behavior, threadIndex, requestID, barrier): 
    
    barrier.wait()  # Wait at barrier for all threads to be up
    try:
        for testIndex in range(numTests):   # iterate through requested tests
            #print(f"\nThread #{threadIndex+1}: Running test {testIndex+1} of {numTests}:")
            requestID = f"Thread {threadIndex+1}, " # reset requestID
            requestID += f"Test {testIndex+1}, "   # add test # to response name
        
            # Run single-persona repo test
            if behavior == "onePers":
                requestID += f"Request 1"  # complete request name
                test_inputfile("testIMs", usePers, requestID) # mode set to test persona input message

             # Run multi-persona repo test of persona input_message files
            elif behavior == "allPers":
                repo_test("testIMs", threadIndex+1, testIndex+1, requestID) # mode set to test persona input messages
            
            # Run single-causal pathway repo test
            if behavior == "oneCP":
                requestID += f"Request 1"  # complete request name
                test_inputfile("testCPs", useCP, requestID) # mode set to test CP input message
            
            # Run multi-message test of causal pathway test suite
            elif behavior == "allCPs":
                repo_test("testCPs", threadIndex+1, testIndex+1, requestID) # mode set to test CP input messages
            
            # Retrieve specified GitHub payload and post
            elif behavior == "customGithub":
                requestID += f"Request 1"  # complete request name
                fullMessage = go_fetch(useGit)      # Retrieve GitHub payload
                post_and_respond(fullMessage, requestID)  # Send POST and respond

            # Build JSON payload from CSV file and post
            elif behavior == "CSV":
                requestID += f"Request 1"  # complete request name
                perfJSON = csv_jsoner(perfPath)
                fullMessage = payloadHeader + perfJSON + payloadFooter
                post_and_respond(fullMessage, requestID)

    
    except Exception as e:
        print(f"{e}")



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

########### Main Script Body ################################
def main():
    print(f"\n\t\tWelcome to the Leakdown Tester, Version {ldtVersion}!")
    try:
        # Set script behavior, readback specified content source
        behavior = set_behavior()
        
        # Determine number of requests to send, readback to user
        calc_total_reqs(behavior)

        # Set API endpoint, readback target URL
        set_target()

        # Create a barrier that waits until all requested threads are up 
        barrier = Barrier(numThreads)


        # Create and run threads based on requested thread number
        threads = []
        for threadIndex in range(numThreads):
            requestID = f"Thread {threadIndex + 1}, "       #Start of new naming plan
            thisThread = threading.Thread(
                target=run_requests,
                args=(behavior, threadIndex, requestID, barrier)
            )
            threads.append(thisThread)
            thisThread.start()
            #print(f"\nThread #{threadIndex+1} started...")

        # Wait for threads to finish running
        for thisThread in threads:
            thisThread.join()


        print("\n\t\tLeakdown test complete.\n")
        exit(0)


    except ValueError as e:
        print(f"{e}")
        exit(1)


if __name__ == "__main__":
    main()