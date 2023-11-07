import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import logging
import base64
import os
import io
## Debugging print module
import pprint

class Pictoralist():
    def __init__(self, performance_dataframe, serialized_perf_df, selected_candidate, settings):
        ## Setup variables to process selected message
        self.performance_data   = performance_dataframe                             # Dataframe of recipient perf data (performance_data_df)
        self.performance_block  = str(serialized_perf_df)                           # Pull un-altered performance (serialized JSON) data to append output messsage with
        self.selected_measure   = str(selected_candidate["measure_name"])           # Name of selected measure
        self.sel_measure_title  = str(selected_candidate["measure_title"])          # Formal name of measure
        self.template_id        = str(selected_candidate["template_id"])            # Message template ID of selected candidate message
        self.display_format     = str(selected_candidate["display"])                # Selected display type
        self.message_text       = str(selected_candidate["message_text"])           # Raw message template fulltext (sans 'Additional message text' (changed 11/6))
        self.comparator_type    = str(selected_candidate["comparator_type"])        # ["Top 25", "Top 10", "Peers", "Goal"] (Peers is peer average?)
        self.acceptable_by      = str(selected_candidate["acceptable_by"])          # Causal pathway determined to be acceptible by
        self.base64_image       = []                                                # Initialize as empty key to later fill image into
        self.staff_ID           = performance_dataframe["staff_number"].iloc[0]     # Preserve one instance of staff number before data cleanup
        self.ghost_frame        = None                                              # placeholder for plotting data voids

        # Config settings from main basesettings class
        self.log_level          = settings.log_level
        self.generate_image     = settings.pictoraless
        self.display_timeframe  = settings.display_window
        self.plot_goal_line     = settings.goal_line
        
        ## IMPLEMENTATION NEEDED ##
        #self.template_name      = str(selected_candidate["template_name"])  # Template text name
            # Semantic name of message template, would be best to implement much earlier in the pipeline, carry it forward

        ### Logging module setup ((WIP))
        # settings.log_level must contain a string like 'INFO' or 'DEBUG'
        log_level = getattr(logging, self.log_level, logging.INFO)
        logging.basicConfig(level=log_level)

        picto_log = logging.StreamHandler()
        picto_log.setLevel(log_level)
        root_logger = logging.getLogger()
        root_logger.addHandler(picto_log)

    # # # # # # # # # # # # Data Setup and Manipulations # # # # # # # # # # # # #

    ### Clean dataframe of non-selected performance data for graph generation, reason on comparator message is about, and make changes to set up graphing
    def prep_data_for_graphing(self):
        ## Initial dataframe shape: 
        # staff_number, measure, month, passed_count, flagged_count, denominator, peer comparators (x3), MPOG_goal, Performance_Rate, comparator_level

        # Only keep rows that contain the measure of interest for this message:
        self.performance_data = self.performance_data[self.performance_data['measure'] == self.selected_measure]
        
        # Initialize new column of data to store only this feedback's crucial comparator levels for graphing as a float:
        self.performance_data["comparator_level"] = 0.0000     # initialize column as float
        self.performance_data["goal_percent"]     = 0.0000     # same as above


        ## Change processing and graphing depending on comparator type:
        # Make changes based on peer 50th percentile benchmark being comparator message "is about"
        if self.comparator_type == "Peer":
            self.performance_data["comparator_level"] = self.performance_data["peer_average_benchmark"]*100 # Select which column of data to keep as the 'comparator_level'
            self.comparator_series_label = "Peer Average"   # Label change for graph legend
        
        # Same as above, but for peer 75th percentile benchmark
        elif self.comparator_type == "Top 25":
            self.performance_data["comparator_level"] = self.performance_data["peer_75th_percentile_benchmark"]*100
            self.comparator_series_label = "Peer Top 25%"
        
        # Same as above, but for peer 90th percentile benchmark
        elif self.comparator_type == "Top 10":
            self.performance_data["comparator_level"] = self.performance_data["peer_90th_percentile_benchmark"]*100
            self.comparator_series_label = "Peer Top 10%"

        # Same as above, but for goal comparator messages
        else:
            self.performance_data["comparator_level"] = self.performance_data["MPOG_goal"]*100.0
            self.comparator_series_label = "Goal Value"


        ## Convert values in selected columns for further processing:
        self.performance_data['month'] = pd.to_datetime(self.performance_data['month'])             # convert month column to datetime objects
        self.performance_data["performance_level"] = self.performance_data["Performance_Rate"]*100.0 # convert preformance ratio to percentage
        self.performance_data["goal_percent"] = self.performance_data["MPOG_goal"]*100.0            # convert MPOG goal ratio to percentage

        ## Drop extraneous columns of current dataframe
        cols_to_keep = ['month', 'measure', 'passed_count', 'denominator', 'performance_level', 'comparator_level','goal_percent']
        self.performance_data = self.performance_data[cols_to_keep]



    ### Fill data voids in the dataset
    def fill_missing_months(self):
        # Sort the DataFrame by the 'month' column
        self.performance_data = self.performance_data.sort_values(by='month')

        # Create a date range for all months between the earliest and latest month
        start_date = self.performance_data['month'].min()
        end_date = self.performance_data['month'].max()
        all_months = pd.date_range(start_date, end_date, freq='MS')

        if len(all_months) != len(self.performance_data['month']):
            logging.info:(f"Data gap(s) detected, filling voids...")
            
            # Make copy of raw data for plotting beneath data gaps if display is a line graph
            if self.display_format == "line_graph":
                self.ghost_frame = self.performance_data.loc[:, ['month', 'performance_level', 'comparator_level']]
                pprint.pprint(self.ghost_frame)
            
            # Reindex the DataFrame with all months and fill missing values
            self.performance_data = self.performance_data.set_index('month').reindex(all_months, fill_value=None).reset_index()
            self.performance_data = self.performance_data.rename(columns={'index': 'month'})  # reset col name from index to month

            # Forward fill 'measure' and percent-scale version of 'MPOG_goal' columns with the previous valid values
            self.performance_data['measure'].fillna(method='ffill', inplace=True)
            self.performance_data['goal_percent'].fillna(method='ffill', inplace=True)


            logging.debug:(f"After gap fill, dataframe is:")
            logging.debug:(self.performance_data)



    ### Fill template text with details for this month's precision feedback message
    def finalize_text(self):
        ## Pull the most recent month's data for generating text feedback:
        current_comparator_percent  = self.performance_data["comparator_level"].iloc[-1]
        current_perf_percent        = self.performance_data["performance_level"].iloc[-1]
        current_perf_passed         = self.performance_data["passed_count"].iloc[-1]
        current_perf_total_cases    = self.performance_data["denominator"].iloc[-1]
        self.init_time              = datetime.datetime.now()                           # Log time when text gen starts



        ## Replace placeholders in the template with actual values
        # Format "[measure name]":
        self.message_text = self.message_text.replace("[measure name]",
        f"{self.selected_measure}: {self.sel_measure_title}"
        )
        # Format "[recipient performance level]":
        self.message_text = self.message_text.replace("[recipient performance level]",
        f"{current_perf_percent:.1f}% ({current_perf_passed}/{current_perf_total_cases} cases)"
        )
        # Format "[comparator performance level]":
        self.message_text = self.message_text.replace("[comparator performance level]", 
        f"{current_comparator_percent:.1f}%"
        )
        ## Insert framework for linking to MPOG measure spec and dashboard link here if task ownership changes



    ### Logic to set display timeframe for graph generation
    def set_timeframe(self):
        #self.display_timeframe = len(self.performance_data)    # Deprecated, now controlled by env var
        logging.info:(f"Dataframe has {self.display_timeframe} months to graph") # Would love to log INFO or DEBUG level
        
        ## Error catcher for windows <3 months
        if self.display_timeframe < 3:
            self.generate_image ==  "false"     # Turn off image generation
            self.display_format == "text_only"  # Set to text-only display type
            logging.warning:("Display format forced to text only by func set_timeframe")
            raise Exception(f"Display Timeframe too small\n\tHow did you do that?")

        ## Hardcoding a policy where bar charts should only show the last 4 months of data:
        if self.display_format == "bar_chart":
            self.display_timeframe = 4

        print(f"Graphing with window of {self.display_timeframe} months")   # Log @ DEBUG once logging handler sorted out



    # # # # # # # # # # # Graphing Functions # # # # # # # # # # # # # #

    ### Modularized plotting and saving shared code for both visual display types:
    def plot_and_save(self):
        plt.tight_layout()
        #plt.show()  # Allow for spot-check of graph locally (not for production)
        plt.savefig(f"cache/display_{self.init_time}.png")            # Save figure locally (redirect if saving images as part of the study I guess?)
        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        return s



    ### Function to generate line chart 
    def generate_linegraph(self):
        # Define the axes, values, and their labels
        y_values = np.arange(0, 101, 20)
        y_labels = [str(val) + '%' for val in y_values]
        x_values = self.performance_data['month'].dt.strftime("%b '%y")
        x_labels = x_values.tolist()

        plt.figure(figsize=(11, 6)) # Create the plot
        
        # Add vertical lines for each month
        for x in x_values:
            plt.axvline(x=x, color='gray', linewidth=0.3)

        # Plot projections of the data if gaps are detected, change line formatting
        if not self.ghost_frame.empty:
            logging.debug('Plotting ghost series...')
            plt.plot(self.ghost_frame['month'].dt.strftime("%b '%y"), self.ghost_frame['performance_level'],
            color='#063763', linestyle='--', linewidth='1')
            plt.plot(self.ghost_frame['month'].dt.strftime("%b '%y"), self.ghost_frame['comparator_level'],
            color='#02b5af', linestyle='--', linewidth='0.75')
        
        # Plot performance and comparator level series
        plt.plot(x_values, self.performance_data["performance_level"], 
            label="You", color="#063763", linewidth=3
        )
        plt.plot(x_values, self.performance_data["comparator_level"], 
            label=self.comparator_series_label, color="#02b5af", linewidth=2
        )
        plt.xticks(rotation=45)

        # Set Axes and plot labels
        plt.yticks(y_values, y_labels)
        plt.ylabel("Performance Level", weight='bold')
        plt.xlabel("Time", weight='bold')
        plt.title(f"Performance Over Time for Measure {self.selected_measure}")

        # Add data labels for the last three months of performance levels as 2 precision floats
        last_three_months = x_values[-3:]
        last_three_performance = self.performance_data["performance_level"][-3:]
        for x, y in zip(last_three_months, last_three_performance):
            # Adjust the xytext parameter to move the label beneath the line
            plt.annotate(f'{y:.2f}%', (x, y), textcoords="offset points",
                weight='bold', xytext=(-5, -20),  # Adjust the offset as needed
                ha='center', fontsize=10.5, color="#063763"
        )

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=1)
        
        # Save and display the graph
        self.base64_image = self.plot_and_save()

 

    ### Function to generate bar chart
    def generate_barchart(self):
        plt.figure(figsize=(10, 6))  # Create figure instance
        bar_width = 0.45             # Arbitrary bar width, adjust to find a good ratio to the display window
        bar_spacing = 0.05
        
        # Define the axes, values, and labels
        y_values = np.arange(0, 101, 20)
        y_labels = [str(val) + '%' for val in y_values]
        x_values = self.performance_data['month'].dt.strftime("%b '%y")
        x_labels = x_values.tolist()

        # Create bars for the timeframe specified by set_timeframe()
        last_x_months = x_values[-self.display_timeframe:]
        series_1_data = self.performance_data["performance_level"][-self.display_timeframe:]
        series_2_data = self.performance_data["comparator_level"][-self.display_timeframe:]

        # Plot the bars for both data series
        x1 = np.arange(len(last_x_months)) + 0.225      # position for first bar
        x2 = [x + bar_width + bar_spacing for x in x1]  # position for second bar
        plt.bar(x1, series_1_data, width=bar_width, label="You", color="#00254a")
        plt.bar(x2, series_2_data, width=bar_width, label=self.comparator_series_label, color="#4d5458")

        # Add data labels for each bar in performance levels
        for x, value in zip(x1, series_1_data):
            index = int(x)  # Cast x to an integer
            if not np.isnan(value):
                label_text = f"{value:.2f}%\n" \
                             f"{self.performance_data['passed_count'].iloc[-self.display_timeframe + index]} / " \
                             f"{self.performance_data['denominator'].iloc[-self.display_timeframe + index]}"
                plt.text(x + bar_width/2, value + 5, label_text, ha='center', va='bottom', fontsize=9, color="#29a3af")

        # Add data labels for each bar in series 2
        for x, value in zip(x2, series_2_data):
            if not np.isnan(value):
                label_text = f"{value:.2f}%"
                plt.text(x + bar_width/2, value + 5, label_text, ha='center', va='bottom', fontsize=9, color="#f3f0ed")


        # If include_goal_line is True, plot the goal line
        if self.plot_goal_line:
            plt.hlines(y=self.performance_data['goal_percent'][-self.display_timeframe:].values, 
               xmin=0, xmax=len(last_x_months)-1, linestyle='--', color='gray', label="Goal"
            )

        # Configure labels, titles, ticks, and limits
        plt.title(f"Performance Over Time for Measure {self.selected_measure}")
        plt.ylabel("Performance Level")
        plt.yticks(y_values, y_labels)
        plt.xlabel("Time")
        plt.xticks(x1 + bar_width / 2, last_x_months, rotation=45)
        plt.ylim(0, 100)
       
        # Format legend and grid
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2)
        plt.grid(False)

        # Save and display the graph
        self.base64_image = self.plot_and_save()




    ### Graphing function control logic (modularized to allow for changes and extra display formats in the future):
    def graph_controller(self):
        if self.display_format == "line_graph":
            print(f"Generating line graph from performance data...")
            self.generate_linegraph()
        
        elif self.display_format == "bar_chart":
            print(f"Generating bar chart from performance data...")
            self.generate_barchart()
        
        else:
            print(f"Generating text only feedback message, graphing skipped...")




    ### Prepare selected message as done previously for LDT continuity:
    def prepare_selected_message(self):
        candidate={}
        message={}
        candidate["message_template_id"]    =self.template_id
        #candidate["message_template_name"]  =self.template_name        # Left for future implementation
        candidate["display"]                =self.display_format
        candidate["measure"]                =self.selected_measure
        candidate["acceptable_by"]          =self.acceptable_by
        message["text_message"]             =self.message_text
        message["measure"]                  =self.selected_measure
        message["measure_full_title"]       =self.sel_measure_title
        #message["message_addtl_text"]       =self.template_addtl_text  # Ditto
        message["image"]                    =self.base64_image

        full_message = {
            "pfkb_version":'0.0.0',     # Need to soft code this so it is accurate
            "pfp_version":'0.2.0 indev',    # Ditto
            "staff_number":self.staff_ID,
            "selected_candidate":candidate,
            "performance_month":self.performance_data["month"].iloc[-1],
            "performance_data":self.performance_block,
            "message_generated_datetime":self.init_time,
            "message":message
        }

        return full_message