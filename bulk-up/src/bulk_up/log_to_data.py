import json
import os
import sys

import pandas as pd
from rdflib import RDFS, Graph, URIRef

# TO Do: make the module path relative
module_path = ".." # run this script from the bulk-up folder. This will add the directory above (which is precision-feedback-pipeline/) to system path to be able to import pipeline modules
sys.path.append(module_path)
from utils.graph_operations import manifest_to_graph
from utils.namespace._IAO import IAO
from utils.namespace._PSDO import PSDO

INPUT_DIR = os.environ.get(
    "INPUT_DIR",
    "/home/faridsei/dev/test/Precision Feedback Message Log 2024-08-20.xlsx",
)
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output.xlsx")
SHEET_NAME = "Sheet1"  # Change this to the name of the sheet in your .xlsx file

df = pd.read_excel(INPUT_DIR, sheet_name=SHEET_NAME, engine="openpyxl")
response_df: pd.DataFrame = pd.DataFrame()

graph: Graph = manifest_to_graph(
    "file:///home/faridsei/dev/code/knowledge-base/mpog_local_manifest.yaml"
)

is_about_to_columns: dict = {
    PSDO.achievement_set: "represented set",
    PSDO.loss_set: "represented set",
    PSDO.approach_set: "represented set",
    PSDO.peer_average_comparator: "comparator content",
    PSDO.peer_75th_percentile_benchmark: "comparator content",
    PSDO.peer_90th_percentile_benchmark: "comparator content",
    PSDO.goal_comparator_content: "comparator content",
    PSDO.social_comparator_element: "comparative element",
    PSDO.goal_comparator_element: "comparative element",
    PSDO.negative_performance_trend_set: "performance trend set",
    PSDO.positive_performance_trend_set: "performance trend set",
    PSDO.negative_performance_gap_set: "performance gap set",
    PSDO.positive_performance_gap_set: "performance gap set",
}

def generate_response(output_message, input_message):
    selected_candidate = output_message.get("selected_candidate", None)
    global response_df
    response_dict: dict = {
        "Performance Month": input_message.get("performance_month", None),
        "Message instance ID": input_message.get("message_instance_id", None),
        "Recipient ID": output_message.get("staff_number", None),
        "Message template ID": selected_candidate["message_template_id"],
        "Message template name": selected_candidate.get(
            "message_template_name", "missing"
        ),
        "represented set": "",
        "performance gap set": "",
        "performance trend set": "",
        "comparative element": "",
        "comparator content": "",
        "causal_pathway": selected_candidate["acceptable_by"],
        "measure": selected_candidate["measure"],
    }

    is_about_set = set(
        graph.objects(URIRef(selected_candidate["message_template_id"]) , IAO.is_about)
    )
    
    if {PSDO.negative_performance_gap_set, PSDO.positive_performance_gap_set} & is_about_set:
        response_dict["represented set"] = "performance gap set"
               
    if {PSDO.negative_performance_trend_set, PSDO.positive_performance_trend_set} & is_about_set:
        response_dict["represented set"] = "performance trend set"

    for is_about in is_about_set:
        if is_about in is_about_to_columns:
            column_name = is_about_to_columns[is_about]
            response_dict[column_name] = graph.value(is_about,RDFS.label).value

    return pd.DataFrame(response_dict)


for index, message in enumerate(df["Output_Message"]):
    if pd.isnull(message):
        continue

    message_parts = message.split(',"image":')
    if len(message_parts) > 1:
        output_message = json.loads(message_parts[0] + "}}")
    else:
        output_message = json.loads(message)

    input_message = json.loads(df.at[index, "Input_Message"].replace("_x000D_", ""))

    new_row = generate_response(output_message, input_message)
    response_df = pd.concat([response_df, new_row ], ignore_index=True)

response_df.to_excel(OUTPUT_DIR, index=False)


## sample code to use signals
# module_path = '/home/faridsei/dev/code/precision-feedback-pipeline/bitstomach/signals/'
# sys.path.append(module_path)
# module_path = '/home/faridsei/dev/code/precision-feedback-pipeline/'
# sys.path.append(module_path)
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
