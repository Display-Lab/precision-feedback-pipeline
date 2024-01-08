import pandas as pd
import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="<b><level>{level}</></> \t{message}")

## Pull in history component of input message for calculations:
def retrieve_history_data(input_message_json):
    logger.trace('Running esteemer.process_history.retrieve_history_data...')
    # Define blank output matrix as a list of dictionaries
    history_component_matrix = []

    # Iterate through items in 'History'
    for month, data in input_message_json['History'].items():
        if data:  # Check if the month has data
            
            # Create a dictionary for each row in the output matrix per month in history
            matrix_row = {
                'Month': month,
                'Measure': data.get('measure', ''),
                'Template Name': data.get('message_template_name', ''),
                'Message Instance ID': data.get('message_instance_id', ''),
                'Message datetime': data.get('message_generated_datetime', ''),
            }
            # Append the row to the output matrix
            history_component_matrix.append(matrix_row)

    # Convert the list of dictionaries to a pandas DataFrame
    outcome_matrix = pd.DataFrame(history_component_matrix)

    # Print the DataFrame (optional, for debugging)
    logger.debug(outcome_matrix)

    return outcome_matrix



## Determine values for history components (measure recency, message recency):
def rank_history_component(acceptable_candidate):

    # 1) Assign time 0 (current feedback month)
    this_month = pd.to_datetime(acceptable_candidate['current_feedback_month'])

    # 2) Define dicts for data output and input
    message_recency_dict = {}
    measure_recency_dict = {}
    history_matrix = retrieve_history_data(acceptable_candidate)

    # 3) Compare row 'month' to t0, convert to integers representing time in months between extant feedback and current month
    history_matrix['Time_Since_t0'] = (
        pd.to_datetime(history_matrix['Month']) - this_month
    ).astype('<m8[M]').astype(int)

    # 4) Calculate message recency
    for candidate in acceptable_candidate:

        # Filter matrix for the specific candidate
        candidate_rows = history_matrix[
            (history_matrix['message_template_name'] == candidate['message_template_name']) &
            (history_matrix['Measure'] == candidate['measure'])
        ]

        # Calculate months since last occurrence of same message
        if not candidate_rows.empty:
            last_occurrence = candidate_rows['Distance_From_t0'].max()
            message_recency_dict[candidate['message_template_name']] = last_occurrence
        else:
            message_recency_dict[candidate['message_template_name']] = None

    # 5) Calculate measure recency
    for candidate in acceptable_candidate:
        candidate_measure = candidate['measure']

        # Filter matrix for the specific candidate measure
        candidate_rows = history_matrix[history_matrix['Measure'] == candidate_measure]

        # Calculate months since last occurrence of same measure
        if not candidate_rows.empty:
            last_occurrence = candidate_rows['Distance_From_t0'].max()
            measure_recency_dict[candidate['measure']] = last_occurrence
        else:
            measure_recency_dict[candidate['measure']] = None

    # Print the recency dictionaries
    logger.debug("Message Recency:", message_recency_dict)
    logger.debug("Measure Recency:", measure_recency_dict)