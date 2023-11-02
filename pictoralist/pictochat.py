import json
import matplotlib.pyplot as plot
import pandas as pd

## Notes:
# Need to have logic statement that fills in data gaps
# before that statement, need to check and verify that there is more than three months of data
# if there is < 3 months of data, force to text only display type and stop image generation
# Line charts need to have option to add in goal lines selectively
# Keep attention to issue 94, handle values as floats at all times when possible


class Pictochat():
    def __init__(performance_dataframe, selected_message, generate_image)
    ## Setup variables to process selected message
    self.performance_data   = performance_dataframe                          # Dataframe of recipient perf data (performance_data_df)
    self.selected_measure   = str(selected_message["Measure Name"])             # Name of selected measure
    self.sel_measure_title  = str(selected_message["Title"])
    self.template_name      = str(selected_message["message_template_name"])     # Template text name
    ## Perhaps unnecessary below, will find replace once pictoralist and templates (re)written and stable
    self.display_format     = str(selected_message["Display"])
    self.message_text       = str(selected_message["text"])
    #self.comparator         = str(selected_message["about_comparator"]) #need team to implement still
    self.comparator         = str()
        # NOTE: self.comparator needs to match the column headers in perf_dataframe
        # Insert code to achieve this here if not done in resolution of Issue #112 work



    ### Clean dataframe of non-selected performance data for graph generation
    def data_cleanup(self):
        ## Initial dataframe shape: 
        # staff_number, measure, month, passed_count, flagged_count, denominator, comparators (x3), MPOG_goal, Performance_Rate
        
        # Only keep rows that contain the measure of interest for this message:
        self.performance_data = self.performance_data[self.performance_data['measure'] == self.selected_message['Measure Name']]

        # Clean columns, remove unnecessary columns for graphing:
        columns_to_keep = ['measure', 'month', 'passed_count', 'denominator', self.comparator, 'MPOG_goal', 'Performance_Rate']
        self.performance_data = self.performance_data[columns_to_keep]

        ## Final dataframe shape:
        # measure, month, passed_count, denominator, X_comparator, MPOG_goal, Performance_Rate



    ### Fill any gaps in the dataset
    def fill_missing_months(self):
        ### Debug:
        # print(self.performance_data)

        # Insert <3 months of data error catcher here?, stop this process and set generate_image to false?
        # Could also catch error in main script


        # Sort the DataFrame by the 'month' column
        self.performance_data['month'] = pd.to_datetime(self.performance_data['month'])
        self.performance_data = self.performance_data.sort_values(by='month')

        # Create a date range for all months between the earliest and latest month
        start_date = self.performance_data['month'].min()
        end_date = self.performance_data['month'].max()
        all_months = pd.date_range(start_date, end_date, freq='MS')

        # Reindex the DataFrame with all months and fill missing values
        self.performance_data = self.performance_data.set_index('month').reindex(all_months, method='ffill', fill_value=0).reset_index()

        # Forward fill 'measure' and 'MPOG_goal' columns with the previous valid values
        self.performance_data['measure'].fillna(method='ffill', inplace=True)
        self.performance_data['MPOG_goal'].fillna(method='ffill', inplace=True)

        ### Debug:
        # print(self.performance_data)



    ### Fill template text with details for this month's precision feedback message
    def finalize_text(self):
        ## Pull the most recent month's data for generating text feedback:
        current_comparator_percent  = self.performance_data[self.comparator].iloc[-1] *100
        current_perf_percent        = self.performance_data["Performance_Rate"].iloc[-1] *100
        current_perf_passed         = self.performance_data["passed_count"].iloc[-1]
        current_perf_total_cases    = self.performance_data["denominator"].iloc[-1]


        ## Replace placeholders in the template with actual values
        # Format "[measure name]":
        self.message_text = self.message_text.replace("[measure name]",
        f"{self.selected_measure}: {self.sel_measure_title}"
        )
        # Format "[recipient performance level]":
        self.message_text = self.message_text.replace("[recipient performance level]",
        f"{current_perf_percent}% ({current_perf_passed}/{current_perf_total_cases} cases)"
        )
        # Format "[comparator performance level]":
        self.message_text = self.message_text.replace("[comparator performance level]", 
        f"{current_comparator_percent}%"
        )
        ## Insert framework for linking to MPOG measure spec and dashboard link here if task ownership changes



    ## Function to generate the graph
    def generate_graphs(self):
        if enable_image:        # Image generation set by flag (pictoraless)
