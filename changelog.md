# PFP Changelog

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