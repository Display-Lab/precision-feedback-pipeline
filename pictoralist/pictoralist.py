import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import base64
import io

### All functions live inside pictoralist class (Mk II, Pictochat: text and display generator)
class Pictoralist():
    def __init__(self, performance_dataframe, serialized_perf_df, selected_candidate, generate_image):
        ## Setup variables to process selected message
        self.performance_data   = performance_dataframe                             # Dataframe of recipient perf data (performance_data_df)
        self.performance_block  = str(serialized_perf_df)                           # Pull un-altered performance (serialized JSON) data to append output messsage with
        self.selected_measure   = str(selected_candidate["measure_name"])           # Name of selected measure
        self.sel_measure_title  = str(selected_candidate["measure_title"])          # Formal name of measure
        self.template_id        = str(selected_candidate["template_id"])            # Message template ID of selected candidate message
        self.display_format     = str(selected_candidate["display"])                # Selected display type
        self.message_text       = str(selected_candidate["message_text"])           # Raw message template fulltext
        self.comparator_type    = str(selected_candidate["comparator_type"])        # ["Top 25", "Top 10", "Peers", "Goal"] (Peers is peer average I believe)
        self.acceptable_by      = str(selected_candidate["acceptable_by"])          # Causal pathway determined to be acceptible by
        self.base64_image       = []                                                # Initialize as empty key to later fill image into
        self.staff_ID           = float(performance_dataframe["staff_number"].iloc[0])  # Preserve one instance of staff number before data cleanup
        
        ## IMPLEMENTATION NEEDED ##
        #self.template_name      = str(selected_candidate["template_name"])  # Template text name
            # Semantic name of message template, would be best to implement much earlier in the pipeline, carry it forward
        self.include_goal_line  = True   
            # Controllable logic flag for including goal line - declare with user preferences? (Todo)



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

        # Same as above, but for goal comparator-based causal pathway messages
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



    ### Fill any gaps in the dataset
    def fill_missing_months(self):
        # Sort the DataFrame by the 'month' column
        self.performance_data = self.performance_data.sort_values(by='month')

        # Create a date range for all months between the earliest and latest month
        start_date = self.performance_data['month'].min()
        end_date = self.performance_data['month'].max()
        all_months = pd.date_range(start_date, end_date, freq='MS')

        # Reindex the DataFrame with all months and fill missing values
        self.performance_data = self.performance_data.set_index('month').reindex(all_months, fill_value=None).reset_index()
        self.performance_data = self.performance_data.rename(columns={'index': 'month'})    # reset col name from index to month

        # Forward fill 'measure' and percent-scale version of 'MPOG_goal' columns with the previous valid values
        self.performance_data['measure'].fillna(method='ffill', inplace=True)
        self.performance_data['goal_percent'].fillna(method='ffill', inplace=True)



    ### Fill template text with details for this month's precision feedback message
    def finalize_text(self):
        ## Pull the most recent month's data for generating text feedback:
        current_comparator_percent  = self.performance_data["comparator_level"].iloc[-1]
        current_perf_percent        = self.performance_data["performance_level"].iloc[-1]
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



    ### Logic to set display timeframe for graph generation
    def set_timeframe(self):
        # TODO: Set up a control variable here that can control this window size and truncate further by request. 
        # Will have to leave the particulars on exactly what conditions set this logic to the team to decide on.
        self.display_timeframe = len(self.performance_data)    # Should return an integer of the size of the dataframe
        print(f"After gap filling, dataframe has {self.display_timeframe} months to graph")
        
        ## Error catcher for windows <3 months
        if self.display_timeframe < 3:
            self.generate_image ==  "false"     # Turn off image generation
            self.display_format == "text-only"  # Set to text-only display type
            print("Display format forced to text-only by func set_timeframe")       #Debug help
            raise Exception(f"Display Timeframe too small!\nSomehow Esteemer has chosen a measure with only one month of data for message delivery\n\tHow did you do that?")

        ## Hardcoding a policy where bar charts should only show the last 4 months of data:
        if self.display_format == "bar chart":
            self.display_timeframe = 4

        print(f"Graphing with window of {self.display_timeframe} months")



    # # # # # # # # # # # Graphing Functions # # # # # # # # # # # # # #

    ### Modularized plotting and saving shared code for both visual display types:
    def plot_and_save(self):
        plt.legend()    # Show legend
        plt.grid()      # Show the graph
        plt.tight_layout()

        plt.show()  # Allow for spot-check of graph locally (not for production)

        plt.savefig("cache/cached1.png")            # Save figure locally (redirect if saving images as part of the study I guess?)
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

        plt.figure(figsize=(10, 6)) # Create the plot
        
        # Add vertical lines for each month
        for x in x_values:
            plt.axvline(x=x, color='gray', linewidth=0.3)
        
        # Plot performance and comparator level series
        plt.plot(x_values, self.performance_data["performance_level"], 
            label="You", color="#063763"
        )
        plt.plot(x_values, self.performance_data["comparator_level"], 
            label=self.comparator_series_label, color="#02b5af"
        )
        plt.xticks(rotation=45)

        # Set Axes and plot labels
        plt.yticks(y_values, y_labels)
        plt.ylabel("Performance Level")
        plt.xlabel("Time")
        plt.title(f"Performance Over Time for Measure {self.selected_measure}")

        # Add data labels for the last three months of performance levels as 2 precision floats
        last_three_months = x_values[-3:]
        last_three_performance = self.performance_data["performance_level"][-3:]
        for x, y in zip(last_three_months, last_three_performance):
            #if not np.isnan(x) and not np.isnan(y) and x != None and y != None:      # Only add data labels for values that exist after gap filling
            plt.annotate(f'{y:.2f}%', (x, y), textcoords="offset points",
                xytext=(0, 10), ha='center', fontsize=8, color="#212121"
            )
        
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
        if self.include_goal_line:
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
       

        # Move the legend outside, center, and at the bottom (not working?)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2)

        # Remove the grid (also not working?)
        plt.grid(False)

        # Save and display the graph
        self.base64_image = self.plot_and_save()




    ### Graphing function control logic (modularized to allow for changes and extra display formats in the future):
    def graph_controller(self):
        if self.display_format == "line graph":
            print(f"Generating line graph from performance data...")
            self.generate_linegraph()
        
        elif self.display_format == "bar chart":
            print(f"Generating bar chart from performance data...")
            self.generate_barchart()
        
        else:
            print(f"Generating text only feedback message, graphing skipped...")




    ### Prepare selected message as done previously for LDT continuity:
    def prepare_selected_message(self):
        candidate={}
        message={}
        candidate["message_template_id"]    =self.template_id
        #candidate["message_template_name"]  =self.template_name
        candidate["display"]                =self.display_format
        candidate["measure"]                =self.selected_measure
        candidate["acceptable_by"]          =self.acceptable_by
        message["text_message"]             =self.message_text
        message["measure"]                  =self.selected_measure
        message["measure_full_title"]       =self.sel_measure_title
        message["image"]                    =self.base64_image

        full_message = {
            "pfkb_version":'0.0.0',     # Need to soft code this
            "pfp_version":'0.2.0 indev',    # Ditto
            "staff_number":self.staff_ID,
            "selected_candidate":candidate,
            "performance_month":self.performance_data["month"].iloc[-1],
            "performance_data":self.performance_block,
            "message_generated_datetime":datetime.datetime.now(),
            "message":message
        }

        return full_message