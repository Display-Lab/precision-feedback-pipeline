# Version 1.1.0
import pandas as pd
import json
import requests
import time
import os
import argparse
import base64
global iniRow,finRow,numCol,reqNumber,target,useGit,showResp,saveResp,perfPath,pfp

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
perfPath =  os.environ.get("CSVPATH")
pfp =       os.environ.get("PFP")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Function to fetch JSON content from GitHub... V8
def go_fetch(url):
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
# think about ninjaing this (whatever that means? ask Peter)
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
        "debug":"no",
        "Preferences":{
            "Utilities": {
            "Motivating_information": 
              {
                "social_better": -5.97766,
                "social_gain":	-2.92114,
                "social_stayed_better":	-12.76936,
                "social_worse":	-0.05277,
                "social_approach":	-0.24384,
                "social_loss":	2.72075,
                "improving":	-0.26266,
                "worsening":	1.06977,
                "social_stayed_worse":	9.97743
              },
            "Display_format":
              {
                "text-only": "0.0",
                "bar_chart": "37.0",
                "line_chart": "0.0"
              }    
          }
        }
    }'''
    return missile

# Function to send the post request...
def send_req(pfp, missile):
	headers = {"Content-Type": "application/json"}
	response = requests.post(pfp, data=missile, headers=headers)
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

if __name__ == "__main__":
    
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

    # Error handling - JSON content source
    if perfPath == None and useGit == None:
        raise ValueError("Please specify where to read JSON content from. See documentation at: ")
    elif perfPath != None and useGit != None:
        print("Warning: JSON payloads specified both via GitHub link and filepath!")
        goOn = input("Do you want to use GitHub input_message as the payload? (y/n)\t")
        if goOn == "n":
            useGit = None
            print("Continuing with CSV JSON payload...")
        else:
            perfPath = None
            print("Continuing with GitHub payload...")

    # Startup messaging
    print("\n\t\tWelcome to the Leakdown Tester!")
    if useGit != None:
        print(f"Reading data from {useGit}...")
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
            sentPost = send_req(pfp, fullMessage)

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
