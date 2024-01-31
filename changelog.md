# PFP Changelog
This project follows 
## Version 0.0.0.22
### Release date: (unreleased)
**Added:** student_t_cleaner to BitStomach
- cleans data of denominators less than ten
- cleans data of measures lacking data for the most recent month's performance
- exits gracefully with 200 code response when no data remains for feedback generation

**Improvement:** Pictoralist: Display functionality fixes 
- Changed strategy for generating annotations on bar chart performance, now using distinct truncated dataframes as in line graphs
- Fixed duplicate logging statements
- Fixed set_timeframe, now functions as intended
- Added conditional annoatation formatting in line and bar displays for low-performance values
- Goal line on bar charts now behind bars

**Changed:** Pictoralist: Display formatting for line graphs and bar charts  
- Fixed resolution at 500x250 w/ 300 dpi  
- Adjusted scaling of visual elements to match new resolution 
- Added alpha channel to figure (testing fully transparent for email implementation)  

**Improvement** Esteemer: Rank candidates for social comparators based on highest comparator performance level 
- When Esteemer finds more than one candidate to be acceptable by social better, select the candidate with the highest comparator performance level 

## Version 0.0.0.21
### Release date: 11/9/23
**Changed:** Settings handling for builds  
- Seperated local and remote env files  
- Created 'settings.py' to handle configuration setting on startup outside main.py  
- Added python-decouple to build requirements (requirements.txt)  
- Removed python-dotenv: requirements, poetry requirements, and settings.py  
- Updated readme with information on setting up a dev .env file and configuring pipeline instances  



**Improvement:** Visual display tweaks to pictoralist
- Changed output to 1 precision float in text message
- Various visual changes to line graph format
- Added functionality to graph data voids with thin dashed lines between continuous data per request
- Various changes to bar chart display format





**Changed:** Pictoralist (major rework)
- Maintain class-based architecture, but operate procedurally
- Implemented data cleanup function to simplify dataframe for plotting
- Implemented gap filling function
- Implemented control logic for setting display timeframe
- Implemented logic to control display detials based on the type of comparator the message is about (goal/social)
- Implemented functions to graph data
- Implemented calls in main to execute successful pictoralist functionality
- Changed Esteemer, Main, Pictoralist to all use snake_case in key values related to communicating between the three
    
## Version 0.0.0.20
**Improvement:**
- Added input messages to the test case folder orginating from MPOG data flow

## Version 0.0.0.19
**Patch:** Improvements to local file startup infrastructure
- Switched from os.listdir to os.scandir for increased effciency
- Note: when specifying local directories for causal pathways and message templates, .env requires the path to be specified without the 'file://' prefix for correct functionality

**Improvement** : Added comprehensive test suite of input messages
- Added test_cases: /pathway_specific and /personas directories
    - Readmes denote structural information about the test cases, as well as expected acceptable candidates and selected candidates by measure for each input message
- CPtests and persona tests can be automatically verified for correctness of overall output using Leakdown Tester

## Version 0.0.0.17
10/9/23  
**Improvement:** Added changelog file  
- Allows tracking changes going forward in pre-release development  
- Compliance <3

**Improvement:** Revised startup behavior; data imports, setup operations of knowledge graphs, environmental variables

- Added comment information to describe the operations on startup from pydantic settings through RDFlib graphing

- Refactored startup graph operations

- Added dotenv support for setting environmental variables from .env file

- Added functionality to scrape github for JSON content on startup
    - Refactored source code for local startup operations is intact (for rollback)

- Removed startup folder now that online knowledge transfer is successful

- Confirmed revised main.py operates as-is on Darwin and Windows OSes, removed windows-specific main.py
    - Have removed need to work with the disperate file systems of OSes by reading from remote data on startup

- Regenerated dependencies in requirements.txt and poetry toml, lock, requirements files

**Improvement:** Enabled pipeline to create precision fieedback without generating images (Pictoraless functionality)  
- Enable with environmental variable "pictoraless", boolean logical
- Var alters instantiation behavior of Pictoralist, should stop the script from starting ready to generate an image
    - This implementaition should be slightly more efficient than controlling all of the logic from the main script  
# Version 0.0.0.16
2/14/2023 
**Improvement:** 
- Complete implementing preferences into the esteemer
- Preferences are implemented based on causal-pathways 
- The preferences were implemented from surveys,each causal pathway will have a number


# Version 0.0.0.15
2/13/2023 
**Improvement:** 
- Intergrated pictoralist basic code into the pipeline, 
- it was not well designed because Zach wanted our concentration mostly on the other stages of the pipeline
- The final picture that got generated is converted to base64 code
- The created picture file is stored in the cached folder
- The basics of output message is created here.
- An example picture was created in the pipeline
-Applying history into the esteemer algorithm

# Version 0.0.0.14
2/7/2023 
**Improvement:** 
- Complete implementing preferences into the esteemer
- Preferences are implemented based on causal-pathways 
- The preferences were implemented from surveys,each causal pathway will have a number

# Version 0.0.0.13
2/6/2023 
**Improvement:** 
- Implement alice message templates and alice causal pathway.
- Implemented Alice endpoint
- Also implemented preferences in the esteemer algorithm
- Major change in the Bit-stomach where the nodes for comparator nodes (peer,goal,top 10,top25)are removed in measure_details.json
- The blank nodes for the comparator nodes(peer,goal,top10,top25) are added in the performer graph
- Get the comparator nodes from performer graph and use it in prepared_data.py

# Version 0.0.0.12
1/31/2023 
**Improvement:** 
- Implement alice message templates and alice causal pathway.
- Both Alice message templates and  alice causal pathways are uploaded into the repository.
- Testing candidate smasher.Accessing the templates annotation into the pipeline
- Getting motivation information from the performer graph in candidate smasher
- The candidate smasher script got decided.

# Version 0.0.0.11
1/27/2023 
**Improvement:** 
- update esteemer to give selected message.
- created "createprecisionfeedback/alice" endpoint which is a precursor to "
"createprecisionfeedback/" endpoint
- The code contains backbone structure used in the endpoint in the main.py

# Version 0.0.0.10
1/27/2023 
**Improvement:** 
- update esteemer to give selected message.
- created "createprecisionfeedback/alice" endpoint which is a precursor to "
"createprecisionfeedback/" endpoint
- The code contains backbone structure used in the endpoint in the main.py

# Version 0.0.0.9
1/25/2023 
**Improvement:** 
- Added basic read me doc. 
- It consists of details how to test the pipeline locally
- Also how to test the pipeline on heroku
- updated poetry.lock 
- updated with requirements.txt
- updated requirements.txt for heroku deployment.



# Version 0.0.0.8
1/25/2023 
**Improvement:** 
- Added basic read me doc. 
- It consists of details how to test the pipeline locally
- Also how to test the pipeline on heroku
- updated poetry.lock 
- updated with requirements.txt
# Version 0.0.0.7
1/24/2023
**Improvement:** 
- Added esteemer stub, that randomly chooses the one of the acceptable by causal pathways into the pipeline.
- Tested the pipeline.Updated the requirements.txt. 
- added poetry packaging tool into the pipeline .


## Version 0.0.0.6  

1/24/2023
**Improvement:** 
- Added esteemer stub, that randomly chooses the one of the acceptable by causal pathways into the pipeline.
- Tested the pipeline.Updated the requirements.txt. 
- added poetry packaging tool into the pipeline .

## Version 0.0.0.5  

1/23/2023
**Improvement:** 
-Intergrated candidate smasher into the pipeline.The candidate smasher is designed that way that used all 4 benchmarks into a single candidate.
-This design was the result of long discussion with the team. 
-Intergrated Thinkpudding into the pipeline. 
-Tested the pipeline and made sure that all the stages are working fine.

## Version 0.0.0.4  

1/16/2023
**Improvement:** 
-Intergrating Bit-stomach into the pipeline.
-Intergrated acheivement_loss.py,consecutive_gap.py,gap_annotate.py,monotinicity_annotate.py,prepare_data_annotate.py,trend_annotate.py
-where each files(cheivement_loss.py,consecutive_gap.py,gap_annotate.py,monotinicity_annotate.py,trend_annotate.py) add the functionality of annotating into the pipeline
-Prepare_data_annotate.py prepares the data that required by the annotation methods and calls them as required.
-Intergrated into main and tested it.


## Version 0.0.0.3  

12/31/2022
**Improvement:** 
-Created Base graph 
-Created performer graph.
-Made sure that the causal pathways 
-templates are imported with read graph method using rdflib method. 
-The skeletal structure of the main.py was made.

## Version 0.0.0.2  

12/29/2022
**Improvement:** 
-Deploying the pipeline in Heroku cloud environment.
-Created requirements.txt.
-added uvicorn worker and 
-gitignore file.


## Version 0.0.0.1  

12/29/2023
**Improvement:** 
-First commit of the precision feedback pipeline.
- This commit consists of consolidated bitstomach,candidate-smasher,thinkpudding and pictoralist in python using FAST API and graphs.
-This is the first commit of consolidated pipeline
