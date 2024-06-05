import json
import os

import pandas as pd

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "")
INPUT_DIR = os.environ.get("INPUT_DIR", "pfp.xlsx")

sheet_name = "Sheet1"  # Change this to the name of the sheet in your .xlsx file
df = pd.read_excel(INPUT_DIR, sheet_name=sheet_name, engine="openpyxl")

all_measures: set = set()

for index, message in enumerate(df["Input_Message"]):
    if pd.isnull(message):
        continue

    # capture all measures
    try:
        message_json = json.loads(message.replace("_x000D_", ""))
    except:
        pn = df.loc[index, "Provider_Number"]
        print(f"could not parse provider {pn}.")
        continue
    perf_data = message_json["Performance_data"]
    perf_data_df = pd.DataFrame(perf_data[1:], columns=perf_data[0])
    measures = perf_data_df["measure"]
    all_measures.update(measures)

    staff_number = message_json["Performance_data"][1][0]

    performance_month = message_json.get("performance_month", None)
    if not performance_month:
        continue

    directory = os.path.join(OUTPUT_DIR, performance_month)
    os.makedirs(directory, exist_ok=True)

    file_name = f"Provider_{staff_number}.json"
    file_path = os.path.join(directory, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(message.replace("_x000D_", "")))
print("Text files have been created for each cell in the 'Input_Message' column.")
print("all measures:\n", set(measures))
