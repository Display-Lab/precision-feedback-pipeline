from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF
from loguru import logger
import pandas as pd
import sys

## Logging setup
logger.remove()
logger.add(sys.stdout, colorize=True, format="{level} | {message}")

### Clean dataframe of measures where statistical significance cannot be determined from analysis
# Shoutout St. James Gate
def student_t_cleaner(perf_dataframe):
    logger.debug(f"Running bit_stomach.student_t_cleaner...")
    # Create a list to store indices of rows to be removed
    cleaned_rows = []

    # Iterate through rows with denominators less than 15
    for index, row in perf_dataframe.iterrows():
        if row['denominator'] < 10:
            cleaned_rows.append(index)

    # Remove rows with insignificant denominators
    if cleaned_rows:
        logger.debug(f'Found rows with non-significant denominators, attempting removal...')
        perf_dataframe.drop(cleaned_rows, inplace=True)
        #logger.debug(f'Cleaned dataframe is: \n{perf_dataframe}')

    # Check if there are at least 3 rows with the same measure after cleaning
    if len(perf_dataframe['measure'].unique()) < 3:
        logger.error(f"Not enough significant data detected in performance block, aborting feedback...")
        raise ValueError("PROCESS_ABORTED")

    return perf_dataframe

