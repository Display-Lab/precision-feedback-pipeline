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

    # Remove rows that need to be cleaned (insignificant denominators, non-current month)
    if cleaned_rows:
        logger.debug(f'Found rows with non-significant denominators, attempting removal...')
        perf_dataframe.drop(cleaned_rows, inplace=True)
        logger.debug(f'Cleaned dataframe is: \n{perf_dataframe}')



    ### Clean measures out that do not have the most recent month of data in them (V9)
    cleaned_rows = [] # Make it blank again, this method sucks
    performance_month = perf_dataframe['month'].max()
    
    # Iterate through measures without the latest month
    for measure in perf_dataframe['measure'].unique():
        measure_rows = perf_dataframe[perf_dataframe['measure'] == measure]
        if performance_month not in measure_rows['month'].unique():
            cleaned_rows.extend(measure_rows.index)

    # Remove rows without the latest month
    if cleaned_rows:
        logger.debug(f'Found measures without the latest month, attempting removal...')
        perf_dataframe.drop(cleaned_rows, inplace=True)
        logger.debug(f'Cleaned dataframe is: \n{perf_dataframe}')




    ## Check if there are no measures with more than 3 unique months after cleaning
    # NOTE: still allows through data for measures with less than 3 months, but if selected we will only get text feedback so that should work.
    if perf_dataframe.groupby('measure')['month'].nunique().max() <= 3:
        logger.error(f"Not enough significant data detected in performance block, aborting feedback...")
        raise ValueError("PROCESS_ABORTED")

    return perf_dataframe

