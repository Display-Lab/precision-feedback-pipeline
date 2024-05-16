import json
import os
from datetime import datetime

import pandas as pd

INPUT_DIR = os.environ.get("INPUT_DIR", "/home/faridsei/dev/test/pfp2.xlsx")
SHEET_NAME = "Sheet1"  # Change this to the name of the sheet in your .xlsx file


def add_response(response_data):
    global response_df

    selected_candidate = response_data.get("selected_candidate", None)
    pm = response_data.get("performance_month", None)
    pm = datetime.strptime(pm, "%B %Y") if pm else "missing"
    response_dict: dict = {
        "staff_number": [response_data.get("staff_number", None)],
        "performance_month": [pm],
        "causal_pathway": selected_candidate["acceptable_by"],
        "measure": selected_candidate["measure"],
        "message": selected_candidate.get("message_template_name", "missing")
        if selected_candidate
        else [None],
    }
    response_df = pd.concat(
        [response_df, pd.DataFrame(response_dict)], ignore_index=True
    )


def analyse_responses():
    global response_df

    causal_pathway = (
        response_df.groupby(["performance_month", "causal_pathway"])["staff_number"]
        .agg(count=("count"))
        .reset_index()
    )

    causal_pathway["monthly_total"] = causal_pathway.groupby("performance_month")[
        "count"
    ].transform("sum")
    causal_pathway["%  "] = round(
        causal_pathway["count"] / causal_pathway["monthly_total"] * 100, 1
    )

    causal_pathway = causal_pathway[
        ["performance_month", "monthly_total", "causal_pathway", "count", "%  "]
    ]
    print(f"\n {causal_pathway} \n")

    message = (
        response_df.groupby(["performance_month", "message"])["staff_number"]
        .agg(count=("count"))
        .reset_index()
    )

    message["monthly_total"] = message.groupby("performance_month")["count"].transform(
        "sum"
    )
    message["%  "] = round(message["count"] / message["monthly_total"] * 100, 1)
    message = message[["performance_month", "monthly_total", "message", "count", "%  "]]

    print(f"\n {message} \n")

    measure = (
        response_df.groupby(["performance_month", "measure"])["staff_number"]
        .agg(count=("count"))
        .reset_index()
    )

    measure["monthly_total"] = measure.groupby("performance_month")["count"].transform(
        "sum"
    )
    measure["%  "] = round(measure["count"] / measure["monthly_total"] * 100, 1)
    measure = measure[["performance_month", "monthly_total", "measure", "count", "%  "]]

    print(f"\n {measure} \n")


df = pd.read_excel(INPUT_DIR, sheet_name=SHEET_NAME, engine="openpyxl")
response_df: pd.DataFrame = pd.DataFrame()

for index, message in enumerate(df["Output_Message"]):
    if pd.isnull(message):
        continue

    message_parts = message.split(',"image":')
    if len(message_parts) > 1:
        message_json = json.loads(message_parts[0] + "}}")
    else:
        message_json = json.loads(message)

    add_response(message_json)

analyse_responses()
