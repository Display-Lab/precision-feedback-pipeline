## Version X.X.X
10/9/23
**Improvement:** Added changelog file

**Improvement:** Revised startup behavior; data imports, setup operations of knowledge graphs, environmental variables

- Added comment information to describe the operations on startup from pydantic settings through RDFlib graphing

- Refactored startup graph operations

- Added dotenv support for setting environmental variables from .env file

- Added functionality to scrape github for JSON content on startup
    - Refactored source code for local startup operations is intact (for rollback protection)

- Removed startup folder now that online knowledge transfer is successful

- Confirmed revised main.py operates as-is on Darwin and Windows OSes
    - Have removed need to work with the disperate file systems of OSes
    - main_windows.py obsolete, removed from repo

- Regenerated dependencies in requirements.txt and poetry toml, lock, requirements files

**Patch:** Added all used measures to PFKB measures.json file