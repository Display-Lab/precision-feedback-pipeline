#Version 1.0.0
import pandas as pd
import json
import requests
import time
global iniRow, finRow, numCol, reqNumber, perfPath, pfp
############### Configure the Following #################################################

iniRow	= 0 		# First row of data to read (!! 0 INDEXED !!)
finRow = 12		# Last row of data to read (Must be contiguous with initial row)
numCol = 10 		# Columns to read in (only change if not using MPOG goals)
reqNumber = 1		# Number of post requests to send the pipeline

## Networking Adjustments ###########
perfPath = "C:\\Users\\galan\\.snakepit\\.Non-pipeline files\\Testing data\\MpogData_Real.csv"	# path to performance data
pfp = "http://127.0.0.1:8000/createprecisionfeedback/"			#Local API endpoint
#pfp = "https://pfpapi.herokuapp.com/createprecisionfeedback/"	#Heroku API endpoint
#pfp = 	"https://pfp.test.app.med.umich.edu/createprecisionfeedback"# GCloud API endpoint in progress, OAuth2.0 protocol knowledge required to use...

#########################################################################################
print("\n\n\t\tWelcome to the Leakdown Tester!")
print("Listing out active configuration settings, please review the following:\n")
print(f"Reading data from {perfPath}...")
print(f"Reading in data with dimensions {numCol} by {finRow - iniRow}...")
print(f"Sending {reqNumber} request(s) to {pfp}...\n")

# Reading in CSV data from file...
def warhead_assembly(path):
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

# Making JSON Payload...
def raytheon(warhead):
    # Step 1: Wrap in header content...
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
    # Step 2: Sneak in our little data package...
    missile += warhead
    # Step 3: Wrap JSON footer around data package...
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
    # Return the final JSON payload
    return missile

# Function to send the post request...
def bombs_away(pfp, missile):
	headers = {"Content-Type": "application/json"}
	response = requests.post(pfp, data=missile, headers=headers)
	return response

if __name__ == "__main__":
    try:
        # Single-function read/write with error checking
        perfJSON = warhead_assembly(perfPath)
        
        # Make the data missile (JSON content of the request)
        amraam = raytheon(perfJSON)

        ###### Manual Message Review #############
        #print("\nJSON missile content:")
        #print(perfJSON)
        #print("\nFull JSON message:")
        #print(amraam)
        ##########################################

        for i in range(reqNumber):
            # Send the POST request(s) to the PFP
            print(f"Trying request {i+1} of {reqNumber}:")
            airtime = time.time()
            fox3 = bombs_away(pfp, amraam)

			# Check response(s)
            if fox3.status_code == 200:
                print("Message delivered in {:.3f} seconds.\n".format(time.time() - airtime))
            else:
                print(f"Delivery failed. Returned status code {fox3.status_code}.")
                print("The missile does not know where it is!\n")
        print("Leakdown Test complete.")

    except ValueError as e:
        print(f"Error: {e}")
