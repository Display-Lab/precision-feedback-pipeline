import os
import sys

import pandas as pd

INPUT = os.environ.get("INPUT", sys.stdin)
df = pd.read_csv(INPUT)

# --------------------------- measures
grouped = df.groupby("staff_number")
unique_measures_ratio = grouped["selected measure"].nunique() / grouped.size()
average_ratio = unique_measures_ratio.mean()
std_dev = unique_measures_ratio.std()
print(
    "The average of the unique measures ratio is:",
    average_ratio,
    " with std: ",
    std_dev,
)

# ---------------------------messages
grouped = df.groupby("staff_number")
unique_messages_ratio = grouped["selected message"].nunique() / grouped.size()
average_ratio = unique_messages_ratio.mean()
std_dev = unique_messages_ratio.std()
print(
    "The average of the unique messages ratio is:",
    average_ratio,
    " with std: ",
    std_dev,
)


# ---------------------------causal pathways
grouped = df.groupby("staff_number")
unique_causal_pathways_ratio = grouped["causal_pathway"].nunique() / grouped.size()
average_ratio = unique_causal_pathways_ratio.mean()
std_dev = unique_causal_pathways_ratio.std()
print(
    "The average of the unique causal_pathways ratio is:",
    average_ratio,
    " with std: ",
    std_dev,
)
