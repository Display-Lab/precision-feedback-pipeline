# PFP Changelog
This project follows [semantic versioning](https://semver.org/spec/v2.0.0.html)!
This changelog format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), conforming as well as possible to the guiding principles.
## [Version 0.2.1]()
### Release date: (unreleased)
**Changed:** 
**Improvement** Rank candidates for social comparators based on highest comparator performance level
- When Esteemer finds more than one candidate to be acceptable by social better, select the candidate with the highest comparator performance level

## Version 0.2.0 [unreleased, no link]
### Release date: (not yet)
**Changed:** Settings handling for builds
- Seperated local and remote env files
    - Heirarchy should help keep dev changes from leaking into production
    - Use a configured copy of .env.devexample for storing your settings when running local instance, and .env.remote should remain unchanged to keep changes in dev from breaking things in the deployments
- Created 'settings.py' to handle configuration setting on startup outside main.py
- Added python-decouple to build requirements (requirements.txt)
- Removed python-dotenv: requirements, poetry requirements, and settings.py
- Updated readme with information on setting up a dev .env file and configuring pipeline instances

**Changed:** Pictoralist strategy for caching images
- Uses slightly altered code from LDT to ensure directory before caching images
    - safer for prod
- Working towards infrastructure changes to maintain cache size at a reasonable level

**Improvement:** Visual display tweaks to pictoralist ([#127](https://github.com/Display-Lab/precision-feedback-pipeline/issues/127))
- Changed output to 1 precision float in text message
- Various visual changes to line graph format
- Added functionality to graph data voids with thin dashed lines between continuous data per request
- Various changes to bar chart display format

**Changed:** Basesettings and environment variable infrastructure
- Moved env vars to basesettings class of pydantic when appropriate
    - Allows conversion of strings in dotenv to other data types like int or bool that can be passed along by basesettings class easily
- Added args to dotenv for controlling display configuration

**Removed:** Debug prints from esteemer node graph of message candidates (to comment)

**Changed:** Pictoralist (major rework)
- Maintain class-based architecture, but operate procedurally
- Implemented data cleanup function to simplify dataframe for plotting
- Implemented gap filling function

- Implemented generative text replacement functionality (Issue [#107](https://github.com/Display-Lab/precision-feedback-pipeline/issues/107))
    - Can use this function (finalize_text) to add links to MPOG spec and dashboard, however should probably be done on MPOG side after recieving the PFP response
        - Need to have access to dashboard link for provider, probably impossible to do in a de-identified way
    - Have hotfixes in the pull request as of 11/5, waiting on approved merge of PFKB template patch for removal of hotfix from pictoralist
        - Tested successfully with update to PFKB files, hotfix removed and committed

- Implemented control logic for setting display timeframe
    - Currently just reports how long the window is set to display by default, and stops image generation if the data shows less than three months
    - Think that this resolves most of [#63](https://github.com/Display-Lab/precision-feedback-pipeline/issues/63)

- Implemented logic to control display detials based on the type of comparator the message is about (goal/social)
    - Requires modifications to data flowing into pictoralist, issue [#112](https://github.com/Display-Lab/precision-feedback-pipeline/issues/112) stuff

- Implemented functions to graph data
    - Needs fairly extensive testing and some further cosmetic modifications, bug fixes highly likely

- Implemented selected_message output building from old pictoralist, minor changes to reflect new variables

- Implemented calls in main to execute successful pictoralist functionality

- Changed Esteemer, Main, Pictoralist to all use snake_case in key values related to communicating between the three
    - See pull request #122, commit hash [ffd411f](https://github.com/Display-Lab/precision-feedback-pipeline/commit/ffd411fc35ea4be24cd395dc90661260132cedd8)

## Version 0.1.2
**Improvement:**
- Added input messages to the test case folder orginating from MPOG data flow

## Version 0.1.1
**Patch:** Improvements to local file startup infrastructure
- Switched from os.listdir to os.scandir for increased effciency
- Note: when specifying local directories for causal pathways and message templates, .env requires the path to be specified without the 'file://' prefix for correct functionality

**Improvement (Development only):** Added comprehensive test suite of input messages
- Added test_cases: /pathway_specific and /personas directories
    - Readmes denote structural information about the test cases, as well as expected acceptable candidates and selected candidates by measure for each input message
- CPtests and persona tests can be automatically verified for correctness of overall output using Leakdown Tester


## Version 0.1.0
**Feature:** Esteemer implemented (initial version)
- Updated files to spec from latest main branch
- Retroactive documentation under development for the new script and its processes  

## Version 0.0.1
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