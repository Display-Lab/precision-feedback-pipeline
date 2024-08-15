import json
import os
from datetime import datetime
import sys
import pandas as pd

INPUT_DIR = os.environ.get("INPUT_DIR", "/home/faridsei/dev/test/pfp2.xlsx")
SHEET_NAME = "Sheet1"  # Change this to the name of the sheet in your .xlsx file


def add_response(output_message, input_message):
    global response_df

    selected_candidate = output_message.get("selected_candidate", None)
    pm = output_message.get("performance_month", None)
    pm = datetime.strptime(pm, "%B %Y") if pm else "missing"
    
    comparator_mapping = {
        "MPOG_goal":"goal_comparator_content",
        "Peer Top 10%":"peer_90th_percentile_benchmark",
        "Peer Top 25%":"peer_75th_percentile_benchmark",
        "Peer Average":"peer_average_comparator"
    }
    
    
    # module_path = '/home/faridsei/dev/code/precision-feedback-pipeline/bitstomach/signals/'
    # sys.path.append(module_path)
    module_path = '/home/faridsei/dev/code/precision-feedback-pipeline/'
    sys.path.append(module_path)
    # from _comparison import Comparison
    # from _trend import Trend
    # from bitstomach.bitstomach import prepare
    # performance_data = eval(output_message.get("performance_data", None))  
    # performance_df = prepare({"Performance_data":performance_data,"performance_month":output_message.get("performance_month", None)})
    # performance_df = performance_df[performance_df["measure"]==output_message["selected_candidate"]["measure"]]
    # comparison = Comparison._detect(performance_df)
    # gap_size = None
    # trend = None
    # try:
    #     trend = Trend._detect(performance_df)
    #     comparison[comparator_mapping[output_message["selected_comparator"]]]
    #     gap_size=round(comparison[comparator_mapping[output_message["selected_comparator"]]][0],3)
    # except:
    #      pass   
    
    from utils.graph_operations import manifest_to_graph
    manifest_to_graph("file:///home/faridsei/dev/code/knowledge-base/mpog_local_manifest.yaml")

    #use templates from the graph here 
    
    response_dict: dict = {
        "Performance Month": input_message.get("performance_month", None),
        "Message instance ID":input_message.get("message_instance_id", None),
        "Recipient ID": output_message.get("staff_number", None),
        "Institution ID":"",
        "Message template ID": selected_candidate["message_template_id"],
        "Message template name": selected_candidate.get("message_template_name", "missing"),
        "Comparator name":comparator_mapping[output_message["selected_comparator"]],
        "causal_pathway": selected_candidate["acceptable_by"],
        "measure": selected_candidate["measure"],
    }
    response_df = pd.concat(
        [response_df, pd.DataFrame(response_dict)], ignore_index=True
    )
    

df = pd.read_excel(INPUT_DIR, sheet_name=SHEET_NAME, engine="openpyxl")
response_df: pd.DataFrame = pd.DataFrame()

for index, message in enumerate(df["Output_Message"]):
    if pd.isnull(message):
        continue

    message_parts = message.split(',"image":')
    if len(message_parts) > 1:
        output_message = json.loads(message_parts[0] + "}}")
    else:
        output_message = json.loads(message)
    
    input_message = json.loads(df.at[index, "Input_Message"].replace("_x000D_", ""))        

    add_response(output_message, input_message)
response_df.to_excel('output.xlsx', index=False)

