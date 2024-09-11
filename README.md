## Precision feedback pipeline

This is the pipeline service that implements the Precision Feedback Pipeline. The underlying model of precision feedback is captured in [this conceptual model](https://onlinelibrary.wiley.com/doi/full/10.1002/lrh2.10419).

Read through our [wiki pages](https://github.com/Display-Lab/precision-feedback-pipeline/wiki) for more detail on testing. Please note that this wiki might not be completely up to date.

### Quick start
This is a Python software project and running the pipeline requires some familiarity with [Python](https://www.python.org/downloads/) and virtual environments. This quick start gives directions using python's built in virtual environment tool [venv](https://docs.python.org/3/library/venv.html) and [Poetry](https://python-poetry.org/).

#### Clone the precision feedback pipeline
```zsh
git clone https://github.com/Display-Lab/precision-feedback-pipeline.git

cd precision-feedback-pipeline
```

#### Setup a virtual environment and install dependencies
**Using `venv` and `pip`**

```zsh
python --version # make sure you have python 3.11
python -m venv .venv
.venv\Scripts\activate.bat # on Windows 
# source .venv/bin/activate  # on Mac or Linux
pip install -r requirements.txt # this will take a while, so go get a cup of coffee
pip install uvicorn # not installed by default (needed for running locally)
```

**Alternative: Using [Poetry](https://python-poetry.org/) (for developers)**

```zsh
poetry env use 3.11 # optional, but makes sure you have python 3.11 available
poetry install # creates a virtual environment and install dependencies
poetry shell # activates the enviroment
```

#### Clone the knowledge base
Clone the knowledge base repository in a separate location 
```zsh
cd ..
git clone https://github.com/Display-Lab/knowledge-base.git 
```

#### Running the pipeline
Change back to the root of precision-feedback-pipeline
```zsh
cd precision-feedback-pipeline
```
Update the `.env.local` file and change `path/to/knowledge-base` to point to the local knowledge base that you just checked out. (Don't remove the `file://` for preferences and manifest.)
```properties
# .env.local
preferences=file:///Users/bob/knowledge-base/preferences.json 
mpm=/Users/bob/knowledge-base/prioritization_algorithms/motivational_potential_model.csv
manifest=file:////Users/bob/knowledge-base/mpog_local_manifest.yaml
...
```

Run the pipeline
```zsh
ENV_PATH=.env.local uvicorn main:app
```

You can use Postman or your favorite tool to send a message and check the results. There is a sample message at `tests/test_cases/input_message.json`. Here is a sample `curl` request:
```zsh
curl --data "@tests/test_cases/input_message.json" http://localhost:8000/createprecisionfeedback/
```

## Environment variables

### Knowledge base settings
Local file path or URL (see .env.remote for github URL formats). All are required.

#### mpm: Path to the mpm csv file

#### preferences: Path to the preferences json file

#### manifest: Path to the manifest file that includes differend pieces of the base graph including (causal pathways, message templates, measures and comparators). See [manifest configuration](#manifest-configuration) for more detail.

### Flags

#### display_window: Maximum number of month to be used to create visual displays (plots)
- default: 6

#### generate_image: If set to true and the display type is bar chart or line chart, then the pipeline will generate the images and include them as part of the response
- default: True

#### log_level: Sets the log level
- default: `WARNING` (this is the production defauslt)
- note: The PFP must be run with **`log_level=INFO`** in order to generate the candidate records in the output. 


#### performance_month: If set, the pipeline will override the performance month in the input requests
- default: None

### Scoring
These control the elements of the scoring algorithm.

#### use_coachiness: Switch to turn on and off coachiness
- default: True

#### use_history: Switch to turn on and off history
- default: True

#### use_mi: Switch to turn on and off motivating information
- default: True

#### use_preferences: Switch to turn on and off preferences
- default: True

### manifest configuration
The manifest file includes all different pieces that should be loaded to the base graph including causal pathways, message templates, measures and comparators. It is a yaml file which specifies a directory structure containing JSON files for all those different categories. 

Each entry consists of a ***key*** which is a URL (file:// or https:// or relative, see [Uniform Resource Identifier (URI)](https://datatracker.ietf.org/doc/html/rfc3986)) and a ***value*** which is a file path relative to the url. See manifest examples in the [knowledge base](https://github.com/Display-Lab/knowledge-base).

If the key is a relative path, it must end with a '/'. In that case the key is going to be resolved towards the location of the manifest file by the pipeline.

### examples
```zsh
 ENV_PATH=/user/.../dev.env log_level=INFO use_preferences=True use_coachiness=True use_mi=True generate_image=False uvicorn main:app --workers=5
```


> :point_right: `uvicorn` can be run with multiple workers. This is useful when testing with a client that can send multiple requests.

