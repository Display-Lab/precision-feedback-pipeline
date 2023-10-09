## Version X.X.X
10/9/23
**Improvement:** Added changelog file

**Patch:** Added all used measures to PFKB measures.json file

**Patch:** Re-wrote data import and setup operations prior to FastAPI app startup

- Added comment information to describe the operations on startup from pydantic settings through RDFlib graphing

- Refactored startup graph operations

- Added dotenv support for setting environmental variables from .env file

- Added functionality to scrape github for JSON content on startup

- Removed startup folder now that online knowledge transfer is successful
