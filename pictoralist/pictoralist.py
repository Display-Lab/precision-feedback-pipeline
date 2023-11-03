import matplotlib.pyplot as plot
import pandas as pd
import datetime
import base64
import numpy
import io

## Notes:
# Need to change all of these json keys to snake_case once the pipeline does so, my lord is it tedious to check cases

### All functions live inside pictoralist class (Mk II, Pictochat: text and display generator)
class Pictoralist():
    def __init__(self, performance_dataframe, serialized_perf_df, selected_candidate, generate_image):
        ## Setup variables to process selected message
        self.performance_data   = performance_dataframe                          # Dataframe of recipient perf data (performance_data_df)
        self.performance_block  = str(serialized_perf_df)   # Pull un-altered performance (serialized JSON) data to append output messsage with
        self.selected_measure   = str(selected_candidate["Measure Name"])#["measure_name"])             # Name of selected measure
        self.sel_measure_title  = str(selected_candidate["Title"])#["title"])
        self.template_name      = "Placeholder Template Name"#str(selected_candidate["message_template_name"])     # Template text name
        self.display_format     = str(selected_candidate["Display"]) #["display"])
        self.message_text       = str(selected_candidate["text"])
        self.comparator_type    = str(selected_candidate["Comparator_Type"])#["comparator_type"])   # ["Top 25", "Top 10", "Peers", "Goal"] (Peers is peer average I believe)
        self.acceptable_by      = str(selected_candidate["Acceptable By"])#["acceptable_by"])
        self.staff_ID           = float(performance_dataframe["staff_number"].iloc[0])  # Preserve one instance of staff number
        ## IMPLEMENTATION NEEDED ##
        self.include_goal_line  = True   
            # Controllable logic flag for including goal line - declare with user preferences? (Todo)

    


    # # # # # # # # # # # # Data Setup and Manipulations # # # # # # # # # # # # #

    ### Clean dataframe of non-selected performance data for graph generation, reason on comparator message is about, and make changes to set up graphing
    def prep_data_for_graphing(self):
        ## Initial dataframe shape: 
        # staff_number, measure, month, passed_count, flagged_count, denominator, peer comparators (x3), MPOG_goal, Performance_Rate, comparator_level

        # Only keep rows that contain the measure of interest for this message:
        self.performance_data = self.performance_data[self.performance_data['measure'] == self.selected_candidate['Measure Name']]
        
        # Initialize new column of data to store only this feedback's crucial comparator levels for graphing as a float:
        self.performance_data["comparator_level"] = 0.0     # initialize column as float

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
            self.performance_data["comparator_level"] = self.performance_data["MPOG_goal"] #redundant, but allows for increased flexibility
            self.comparator_series_label = "Goal Value"
        
        ## Drop columns 7-9 of current dataframe (peer comparators)
        self.performance_data = self.performance_data.drop(self.performance_data.columns[7:10], axis=1)

        ## Convert month column to datetime format for further processing:
        self.performance_data['month'] = pd.to_datetime(self.performance_data['month'])

        ## Convert performance ratio to percentage for whole column:
        self.performance_level = self.performance_data["Performance_Rate"]*100

        ## Final dataframe shape:
        # measure, month, passed_count, denominator, MPOG_goal, Performance_Rate, comparator_level



    ### Fill any gaps in the dataset
    def fill_missing_months(self):
        ### Debug:
        print(f"Starting fill_missing_months...\n{self.performance_data}")

        # Sort the DataFrame by the 'month' column
        self.performance_data = self.performance_data.sort_values(by='month')

        # Create a date range for all months between the earliest and latest month
        start_date = self.performance_data['month'].min()
        end_date = self.performance_data['month'].max()
        all_months = pd.date_range(start_date, end_date, freq='MS')

        # Reindex the DataFrame with all months and fill missing values
        self.performance_data = self.performance_data.set_index('month').reindex(all_months, fill_value='0.0').reset_index()

        # Forward fill 'measure' and 'MPOG_goal' columns with the previous valid values
        self.performance_data['measure'].fillna(method='ffill', inplace=True)
        self.performance_data['MPOG_goal'].fillna(method='ffill', inplace=True)

        ### Debug:
        print(f"fill_missing_months complete...\n{self.performance_data}")



    ### Fill template text with details for this month's precision feedback message
    def finalize_text(self):
        ## Pull the most recent month's data for generating text feedback:
        current_comparator_percent  = self.performance_data["comparator_level"].iloc[-1]
        current_perf_percent        = self.performance_data["Performance_Rate"].iloc[-1]
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
        # NOTE: fill_missing_months is set up to only fill months BETWEEN extant data, so . Will set up a control variable
        #  here that can control this window size and truncate further by request. Will have to leave the particulars
        #  on exactly what conditions set this logic to the team to decide on.
        self.display_timeframe = len(self.performance_data)    # Should return an integer of the size of the dataframe
        print(f"Display timeframe starts at {self.display_timeframe} months")
        
        ## Error catcher for windows <3 months
        if self.display_timeframe < 3:
            self.generate_image ==  "false"     # Turn off image generation
            self.display_format == "text-only"  # Set to text-only display type
            print("Display format forced to text-only by func set_timeframe")       #Debug help
            raise Exception(f"Display Timeframe too small!\nSomehow Esteemer has chosen a measure with only one month of data for message delivery\n\tHow did you do that?")



    # # # # # # # # # # # Graphing Functions # # # # # # # # # # # # # #

    ### Modularized plotting and saving shared code for both visual display types:
    def plot_and_save():
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
        # Define the Y-axis data
        y_values = np.arange(0, 101, 20)
        y_labels = [str(val) + '%' for val in y_values]

        # Define the X-axis data (months) and labels
        x_values = self.performance_data['month'].dt.strftime("%b '%y")
        x_labels = x_values.tolist()

        # Create the plot
        plt.figure(figsize=(10, 6))
        
        # Add vertical lines for each month
        for x in x_values:
            plt.axvline(x=x, color='gray', linewidth=0.3)
        
        # Plot series 1 and 2
        plt.plot(x_values, self.performance_level, label="You", marker='o')
        plt.plot(x_values, self.comparator_level, label=self.comparator_series_label, linestyle='--', marker='x')
        plt.xticks(rotation=45)

        # Set Axes and plot labels
        plt.yticks(y_values, y_labels)
        plt.ylabel("Performance Level")
        plt.xlabel("Time")
        plt.title(f"Performance Over Time for Measure {self.selected_measure}")

        # Add data labels for the last three months of performance levels as 2 precision floats
        last_three_months = x_values[-3:]
        last_three_performance = self.performance_level[-3:]
        for x, y in zip(last_three_months, last_three_performance):
            plt.annotate(f'{y:.2f}%', (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)
        
        # Save and display the graph
        self.base64_image = plot_and_save()

 

    ### Function to create bar chart for feedback message:
    def generate_barchart(self):
        # Define the Y-axis data
        y_values = np.arange(0, 101, 20)
        y_labels = [str(val) + '%' for val in y_values]

        # Define the X-axis data (months) and labels
        x_values = self.performance_data['month'].dt.strftime("%b '%y")
        x_labels = x_values.tolist()

        # Create the plot
        plt.figure(figsize=(10, 6))

        # Set axes labels
        plt.ylabel("Performance Level")
        plt.yticks(y_values, y_labels)
        plt.xlabel("Time")
        plt.xticks(rotation=45)
        plt.title(f"Performance Over Time for Measure {self.selected_measure}")

        # Create bars for the timeframe specified by set_timeframe()
        last_x_months = x_values[-self.display_timeframe:]
        series_1_data = self.performance_level[-self.display_timeframe:]
        series_2_data = self.comparator_level[-self.display_timeframe:]

        # Plot the bars for series 1 and 2
        plt.bar(last_x_months, series_1_data, label="You")
        plt.bar(last_x_months, series_2_data, label=self.comparator_series_label)

        # Add data labels for each bar in series 1
        for i in range(len(last_x_months)):
            label_text = f"{self.performance_dataframe['Performance_Rate'].iloc[-self.display_timeframe + i]:.2f}% " \
                         f"({self.performance_dataframe['passed_count'].iloc[-self.display_timeframe + i]}/" \
                         f"{self.performance_dataframe['denominator'].iloc[-self.display_timeframe + i]})"
            plt.text(last_x_months[i], series_1_data[i] + 5, label_text, ha='center', va='bottom')

        # Add data labels for each bar in series 2
        for i in range(len(last_x_months)):
            plt.text(last_x_months[i], series_2_data[i] + 5, f"{series_2_data[i]:.2f}", ha='center', va='bottom')

        # If include_goal_line is True, plot the goal line
        if self.include_goal_line:
            goal_data = self.performance_data['MPOG_goal'][-self.display_timeframe:]
            plt.plot(last_x_months, goal_data, linestyle='--', color='gray', label="Goal")

        # Save and display the graph
        self.base64_image = plot_and_save()



    ### Graphing function control logic (modularized to allow for changes and extra display formats in the future):
    def graph_controller(self):
        if self.display_format == "line graph":
            print(f"Generating line graph from performance data...")
            generate_linegraph(self)
        
        elif self.display_format == "bar chart":
            print(f"Generating bar chart from performance data...")
            generate_barchart(self)
        
        else:
            print(f"Generating text only feedback message, graphing skipped...")




    ### Prepare selected message as done previously for LDT continuity:
    def prepare_selected_message(self):
        candidate={}
        message={}
        candidate["message_template"]=self.template_name
        candidate["display"]=self.display_format
        candidate["measure"]=self.measure_name
        candidate["acceptable_by"]=self.acceptable_by
        message["text_message"]=self.message_text
        message["measure"]=self.measure_name
        message["measure_full_title"]=self.sel_measure_title
        message["image"]=self.base64_image

        full_message = {
            "staff_number":self.staff_ID,
            "selected_candidate":candidate,
            "performance_data":self.performance_block,
            "performance_month":performance_dataframe["month"].iloc[-1],
            "message_generated_datetime":datetime.datetime.now(),
            "pfkb_version":'0.0.0',     # Need to soft code in the morning...
            "pfp_version":'0.2.0 indev',    # Ditto
            "Message":message
        }

        return full_message