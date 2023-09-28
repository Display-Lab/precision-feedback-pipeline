## Version X.X.X
**Improvement:** Added changelog file

**Patch:** Added all used measures to local measures.json and PFKB version

**Patch:** Re-wrote data import and setup operations prior to FastAPI app startup

- Added comment information to describe the operations on startup from pydantic settings through RDFlib graphing
    - Renamed variables from 'asa...' and 'list...' to better describe the objects represented by said vars
        - asa and asaa sunset by refactored list operation
        - list2 -> pathway_list
        - list3 -> template_list

- Attempted to add logging module for startup debug, however FastAPI logging ignores log handler so statements are not printed. Removed.

- Refactored startup graph operations
    - Do have questions still about some lines of code and their necessity
    - unique identifiers in new function 'directory_to_graph'

- Added dotenv support for setting environmental variables from .env file
    - Added .env file to .gitignore
        - Will need to have individuals write their own .env files, but better than having on the github repo!

- Added functionality to scrape github for JSON content on startup
    - use links formatted like below when setting up .env:
    "https://api.github.com/repos/Display-Lab/knowledge-base/contents/causal_pathways"