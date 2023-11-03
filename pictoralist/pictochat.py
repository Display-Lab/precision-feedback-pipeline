import json
import matplotlib.pyplot as plot
import pandas as pd

## Notes:
# Need to have logic statement that fills in data gaps
# before that statement, need to check and verify that there is more than three months of data
# if there is < 3 months of data, force to text only display type and stop image generation
# Line charts need to have option to add in goal lines selectively
# Keep attention to issue 94, handle values as floats at all times when possible
#
# Need to change all of these json keys to snake_case once the pipeline does so, my lord is it tedious to check cases


class Pictochat():
    def __init__(performance_dataframe, selected_message, generate_image)
    ## Setup variables to process selected message
    self.performance_data   = performance_dataframe                          # Dataframe of recipient perf data (performance_data_df)
    self.selected_measure   = str(selected_message["Measure Name"])             # Name of selected measure
    self.sel_measure_title  = str(selected_message["Title"])
    self.template_name      = str(selected_message["message_template_name"])     # Template text name
    self.display_format     = str(selected_message["Display"])
    self.message_text       = str(selected_message["text"])

    ## IMPLEMENTATION NEEDED ##
    self.include_goal_line  = True   
        # Controllable logic flag for including goal line - declare with user preferences? (Todo)

    self.comparator_type    = str(selected_message["comparator_type"]) 
        # IE: "goal comparator element" OR "social comparator element"
        # Comes from the message template's "is_about"/elements (goal comp element or soc comp el.)
        # Used to change aspects of plots to visualize goal comparisons accurately

    self.about_comparator   = str(selected_message["about_comparator"])  
        # Name of comparator used by message, ex "peer average benchmark"
        # Comes from message template's "is_about"/benchmark
        # NOTE: Key DNE for goal-based messages, should be set 'None' in those cases
    
    
    


    # # # # # # # # # # # # Data Setup and Manipulations # # # # # # # # # # # # #

    ### Clean dataframe of non-selected performance data for graph generation
    def performance_data_cleanup(self):
        ## Initial dataframe shape: 
        # staff_number, measure, month, passed_count, flagged_count, denominator, comparators (x3), MPOG_goal, Performance_Rate
        
        ## Only keep rows that contain the measure of interest for this message:
        self.performance_data = self.performance_data[self.performance_data['measure'] == self.selected_message['Measure Name']]


        ## Clean columns based on what pathway flavor is in use:
        # Define the common columns to keep
        columns_to_keep = ['measure', 'month', 'passed_count', 'denominator', 'MPOG_goal', 'Performance_Rate']

        # Append comparator levels if pathway is social comp reliant
        if self.comparator_type == "social comparator element":
            columns_to_keep.append(self.about_comparator.lower().replace(' ', '_'))

        # Filter the dataframe to keep only the specified columns
        self.performance_data = self.performance_data[columns_to_keep]


        ## Convert month column to datetime format for further processing:
        self.performance_data['month'] = pd.to_datetime(self.performance_data['month'])

        ## Convert performance ratio to percentage for whole column:
        self.performance_level = self.performance_data["Performance_Rate"]*100

        ## Define comparator level changes for graphing:
        self.comparator_level = self.performance_data[self.is_about_comp]*100

        ## Final dataframe shape:
        # measure, month, passed_count, denominator, [X_comparator,] MPOG_goal, Performance_Rate



    ### Fill any gaps in the dataset
    def fill_missing_months(self):
        ### Debug:
        print(f"Starting fill_missing_months...\n{self.performance_data}")

        # Insert <3 months of data error catcher here?, stop this process and set generate_image to false?
        # Could also catch error in main script


        # Sort the DataFrame by the 'month' column
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
        print(f"fill_missing_months complete...\n{self.performance_data}")



    ### Fill template text with details for this month's precision feedback message
    def finalize_text(self):
        ## Pull the most recent month's data for generating text feedback:
        current_comparator_percent  = self.performance_data[self.is_about_comp].iloc[-1] *100
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
        self.display_timeframe = len.(self.performance_data)    # Should return an integer of the size of the dataframe
        print(f"Display timeframe starts at {self.display_timeframe} months")
        
        ## Error catcher for windows <3 months
        if self.display_timeframe < 3:
            self.generate_image ==  "false"     # Turn off image generation
            self.display_format == "text-only"  # Set to text-only display type
            print("Display format forced to text-only by func set_timeframe")       #Debug help
            raise Exception(f"Display Timeframe too small!\nSomehow Esteemer has chosen a measure with only one month of data for message delivery\n\tHow did you do that?")



    # # # # # # # # # # # Graphing Functions # # # # # # # # # # # # # #
    
    ### Modular text alteration of graph elements for social vs goal comparisons:
    def comparator_switch(self):
        # Set text for series name based on if using goal comparator
        if comparator_type == "goal"
            self.comparator_series_label = "Goal Value"
        # Default to social comparator if anything but goal specified above, set labels by comparator 
        else:
            if self.about_comparator == "peer average comparator":
                self.comparator_series_label = "Peer Average"
            
            elif self.about_comparator == "peer 75th percentile benchmark":
                self.comparator_series_label = "Peer Top 25%"
            
            elif self.about_comparator == "peer 90th percentile benchmark":
                self.comparator_series_label = "Peer Top 10%"


    ### Modularized plotting and saving shared code for both visual display types:
    # NOTE: this may be a touchy boy, SHOULD scope properly if following matlab rules, however if we 
    # make changes that ALTER the plt object's global definition, it will anger the machine spirit
    def plot_and_save():
        # Show legend
        plt.legend()

        # Show the graph
        plt.grid()
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
        comparator_switch(self)

        # Define the Y-axis data
        y_values = np.arange(0, 101, 20)
        y_labels = [str(val) + '%' for val in y_values]

        # Define the X-axis data (months) and labels
        x_values = self.performance_data['month'].dt.strftime("%b '%y")
        x_labels = x_values.tolist()

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, self.performance_level, label="You", marker='o')
        plt.plot(x_values, self.comparator_level, label=self.comparator_series_label, linestyle='--', marker='x')
        plt.xticks(rotation=45)

        # Set Axes and plot labels
        plt.yticks(y_values, y_labels)
        plt.ylabel("Performance Level")
        plt.xlabel("Time")
        plt.title(f"Performance Over Time for Measure {self.comparator_name}")

        # Add vertical lines for each month
        for x in x_values:
            plt.axvline(x=x, color='gray', linewidth=0.5)

        # Add data labels for the last three months of performance levels as integer-ized floats
        last_three_months = x_values[-3:]
        last_three_performance = self.performance_level[-3:]
        for x, y in zip(last_three_months, last_three_performance):
            plt.annotate(f'{y:.2f}%', (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

        # Code below has been modularized, only remove string literals if testing fails d/t scoping
        '''
        # Show legend
        plt.legend()

        # Show the graph
        plt.grid()
        plt.tight_layout()
        plt.show()  #debug only
        # Save figure locally (redirect for )
        plt.savefig("cache/cached1.png")
        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        '''
        # Delete above string literal code when passes testing if modularity working
        
        # Previously, had this func returning the graph to store as a key in main, doesn't get used otherwise?
        # We can just throw it in as a key in this class and return it with the rest of the content at the end of the script now
        self.base64_image = plot_and_save()

 




    ### Graphing function control logic (modularized to allow for changes and extra display formats in the future):
    def graph_controller(self):
        if self.comparator_type == "goal":
            # Change the vars controlling what comparator is being graphed from benchmark to goal line
            # Change var titling series in the graph generation

        if self.display_format == "line graph":
            print(f"Generating line graph from performance data...")
            generate_linegraph(self)
        
        elif self.display_format == "bar chart":
            print(f"Generating bar chart from performance data...")
            generate_barchart(self)
        
        else:
            print(f"Generating text only feedback message...")