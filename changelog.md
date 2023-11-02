# PFP Changelog
## Version 0.2.0 (indev)
**Improvement:** Rework Pictoralist (pictochat.py for dev work)
- Maintain class-based architecture, but operate procedurally
- Implemented data cleanup function to simplify dataframe for use in pictoralist
- Implemented gap filling function
    - See issue [#110](https://github.com/Display-Lab/precision-feedback-pipeline/issues/110)
    - Still thinking about best way to check error about < 3 months of data, could implement here and assert data length, could also implement in main.py 
    - Above is contingent on that bug still being present in the new script, can't tell until we have 'about_comparator' and 'message_template_name' key changes made and we enter testing phase (resolve issue [#112](https://github.com/Display-Lab/precision-feedback-pipeline/issues/112) first)

- Adding generative text replacement functionality (Issue [#107](https://github.com/Display-Lab/precision-feedback-pipeline/issues/107))


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