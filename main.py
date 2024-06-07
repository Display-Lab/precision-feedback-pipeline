import csv
import json
import os
import sys
import time
import webbrowser
from datetime import timedelta
from io import StringIO
from pathlib import Path

import matplotlib
import psutil
import requests
from fastapi import FastAPI, HTTPException, Request
from loguru import logger
from rdflib import (  # , ConjunctiveGraph, Namespace, URIRef, RDFS, Literal
    RDF,
    BNode,
    Graph,
    Literal,
    URIRef,
)
from requests_file import FileAdapter

from bitstomach import bitstomach
from candidate_pudding import candidate_pudding
from esteemer import esteemer, utils
from pictoralist.pictoralist import Pictoralist
from utils.graph_operations import read_graph
from utils.namespace import PSDO, SLOWMO
from utils.settings import settings

matplotlib.use("Agg")


logger.info(
    f"Initial system memory: {psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024}"
)

### Logging module setup (using loguru module)
logger.remove()
logger.add(
    sys.stdout, colorize=True, format="{level}|  {message}", level=settings.log_level
)
logger.at_least = (
    lambda lvl: logger.level(lvl).no >= logger.level(settings.log_level).no
)

## Log of instance configuration
logger.debug("Startup configuration for this instance:")
for attribute in dir(settings):
    if not attribute.startswith("__"):
        value = getattr(settings, attribute)
        logger.debug(f"{attribute}:\t{value}")


### Create RDFlib graph from locally saved json files
def local_to_graph(thisDirectory, file_list = None):
    g: Graph = Graph()
    logger.debug("Starting function local_to_graph...")

    if file_list:
        with open(file_list, "r") as file:
            json_only = [
                os.path.join(thisDirectory,entry)
                for entry in json.load(file)            
            ]
    else:        
        # Scrape directory, filter to only JSON files, build list of paths to the files (V2)
        json_only = [
            entry.path
            for entry in os.scandir(thisDirectory)
            if entry.name.endswith(".json")
        ]

    # Iterate through list, parsing list information into RDFlib graph object
    for n in range(len(json_only)):
        temp_graph = Graph()  # Creates empty RDFlib graph
        temp_graph.parse(
            json_only[n], format="json-ld"
        )  # Parse list data in JSON format
        logger.debug(f"Graphed file {json_only[n]}")
        g = g + temp_graph  # Add parsed data to graph object
    return g


### Create RDFlib graph from remote knowledgebase JSON files
def remote_to_graph(contentURL, file_list = None):
    g: Graph = Graph()

    logger.debug("Starting function remote_to_graph...")

    # Fetch JSON content from URL (directory)
    response = requests.get(contentURL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch JSON content from URL: {contentURL}")

    try:
        contents = response.json()
        
        if file_list:
            file_list_response = requests.get(file_list)
            file_list = file_list_response.json()
        
        for item in contents:
            file_name = item["name"]
            if file_list and file_name not in file_list:
                continue
                
            if file_name.endswith(".json"):  # Check if the file has a .json extension
                file_jsoned = json.loads(
                    requests.get(item["download_url"]).content
                )  # Download content, store as JSON
                temp_graph = Graph().parse(
                    data=json.dumps(file_jsoned), format="json-ld"
                )  # Parse JSON, store as graph
                logger.debug(f"Graphed file {file_name}")
                g += temp_graph

    except json.JSONDecodeError:
        raise Exception("Failed parsing JSON content.")

    return g


### read csv file to a dictionary
def load_mpm() -> dict:
    mpm_dict = {}

    if settings.mpm.startswith("http"):
        response = requests.get(settings.mpm)
        response.raise_for_status()
        csv_content = StringIO(response.text)
        file = csv_content
    else:
        file = open(settings.mpm, mode="r")

    reader = csv.DictReader(file)
    for row in reader:
        outer_key = row.pop("causal_pathway")
        mpm_dict[outer_key] = {
            k: (float(v) if v != "" else None) for k, v in row.items()
        }

    if not settings.mpm.startswith("http"):
        file.close()

    return mpm_dict


# Set up request session as se, config to handle file URIs with FileAdapter
se = requests.Session()
se.mount("file://", FileAdapter())
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    try:
        global \
            comparators_graph, \
            measures_graph, \
            mpm, \
            default_preferences, \
            causal_pathways_graph, \
            templates_graph

        measures_text = se.get(settings.measures).text
        measures_graph = read_graph(measures_text)

        comparators_text = se.get(settings.comparators).text
        comparators_graph = read_graph(comparators_text)

        mpm = load_mpm()

        preferences_text = se.get(settings.preferences).text
        default_preferences = json.loads(preferences_text)

        ### Changes loading strategy depending on the source of PFKB content
        if not settings.pathways.startswith("http"):
            # Build graphs with local os.dirname method if using file URI
            causal_pathways_graph = local_to_graph(settings.pathways)
        else:
            # Build graphs from remote resource if using URLs
            causal_pathways_graph = remote_to_graph(settings.pathways)

        if not settings.templates.startswith("http"):
            # Build graphs with local os.dirname method if using file URI
            templates_graph = local_to_graph(settings.templates, settings.templates_local)
        else:
            # Build graphs from remote resource if using URLs
            templates_graph = remote_to_graph(settings.templates, settings.templates_local)


    except Exception as e:
        print("Startup aborted, see traceback:")
        raise e


@app.get("/")
async def root():
    return {"Hello": "Universe"}


@app.get("/info")
async def info():
    return settings


@app.get("/template/")
async def template():
    github_link = "https://raw.githubusercontent.com/Display-Lab/precision-feedback-pipeline/main/input_message.json"
    return webbrowser.open(github_link)


@app.post("/createprecisionfeedback/")
async def createprecisionfeedback(info: Request):
    req_info = await info.json()

    if settings.performance_month:
        req_info["performance_month"] = settings.performance_month

    preferences = set_preferences(req_info)

    initial_tic = tic = time.perf_counter()

    cool_new_super_graph = Graph()
    cool_new_super_graph += comparators_graph
    cool_new_super_graph += causal_pathways_graph
    cool_new_super_graph += measures_graph
    cool_new_super_graph += templates_graph

    toc = time.perf_counter()
    timing = {"load base graph": f"{(toc-tic)*1000.:2.2f} ms"}
    debug_output_if_set(cool_new_super_graph, "outputs/base.json")

    # BitStomach
    logger.debug("Calling BitStomach from main...")

    tic = time.perf_counter()
    performance_data_df = bitstomach.prepare(req_info)
    # TODO: find a place for measures to live...mabe move these two line into prepare or make a measurees class
    measures = set(cool_new_super_graph[: RDF.type : PSDO.performance_measure_content])

    performance_data_df.attrs["valid_measures"] = [
        m for m in performance_data_df.attrs["valid_measures"] if BNode(m) in measures
    ]
    g: Graph = bitstomach.extract_signals(performance_data_df)

    performance_content = g.resource(BNode("performance_content"))
    if len(list(performance_content[PSDO.motivating_information])) == 0:
        cool_new_super_graph.close()
        detail = {
            "message": "Insufficient significant data found for providing feedback, process aborted.",
            "message_instance_id": req_info["message_instance_id"],
            "staff_number": performance_data_df.attrs["staff_number"],
        }
        raise HTTPException(
            status_code=400,
            detail=detail,
            headers={"400-Error": "Invalid Input Error"},
        )

    cool_new_super_graph += g
    toc = time.perf_counter()
    timing["extract signals"] = f"{(toc-tic)*1000.:.2f} ms"

    debug_output_if_set(cool_new_super_graph, "outputs/spek_bs.json")

    # candidate_pudding
    logger.debug("Calling candidate_pudding from main...")
    tic = time.perf_counter()
    candidate_pudding.create_candidates(cool_new_super_graph)
    toc = time.perf_counter()
    timing["create candidates"] = f"{(toc-tic)*1000.:.2f} ms"

    # #Esteemer
    logger.debug("Calling Esteemer from main...")
    history: dict = req_info.get("History", {})
    history = {
        key: value
        for key, value in history.items()
        if key < performance_data_df.attrs["performance_month"]
    }

    tic = time.perf_counter()
    measures: set[BNode] = set(
        cool_new_super_graph.objects(
            None, PSDO.motivating_information / SLOWMO.RegardingMeasure
        )
    )
    for measure in measures:
        candidates = utils.candidates(
            cool_new_super_graph, filter_acceptable=True, measure=measure
        )
        for candidate in candidates:
            esteemer.score(candidate, history, preferences["Message_Format"], mpm)
    selected_candidate = esteemer.select_candidate(cool_new_super_graph)
    if preferences["Display_Format"]:
        cool_new_super_graph.resource(selected_candidate)[SLOWMO.Display] = Literal(
            preferences["Display_Format"]
        )
    toc = time.perf_counter()
    timing["esteemer"] = f"{(toc-tic)*1000.:.2f} ms"

    # print updated graph by esteemer
    debug_output_if_set(cool_new_super_graph, "outputs/spek_st.json")

    tic = time.perf_counter()
    selected_message = utils.render(cool_new_super_graph, selected_candidate)

    ### Pictoralist 2, now on the Nintendo DS: ###
    logger.debug("Calling Pictoralist from main...")
    if selected_message["message_text"] != "No message selected":
        ## Initialize and run message and display generation:
        tic = time.perf_counter()
        pc = Pictoralist(
            performance_data_df,
            req_info["Performance_data"],
            selected_message,
            settings,
            req_info["message_instance_id"],
        )
        pc.prep_data_for_graphing()  # Setup dataframe of one measure, cleaned for graphing
        pc.fill_missing_months()  # Fill holes in dataframe where they exist
        pc.set_timeframe()  # Ensure no less than three months being graphed
        pc.finalize_text()  # Finalize text message and labels
        pc.graph_controller()  # Select and run graphing based on display type

        full_selected_message = pc.prepare_selected_message()
    else:
        full_selected_message = selected_message

    toc = time.perf_counter()
    timing["pictoralist"] = f"{(toc-tic)*1000.:.2f} ms"
    timing["total"] = timedelta(seconds=(toc - initial_tic))

    response = {}
    # if settings.log_level == "INFO":
    if logger.at_least("INFO"):
        response["timing"] = timing

        # Get memory usage information
        mem_info = psutil.Process(os.getpid()).memory_info()

        response["memory (RSS in MB)"] = {
            "memory_info.rss": mem_info.rss / 1024 / 1024,
        }

        cool_new_super_graph.add(
            (
                BNode("p1"),
                URIRef("http://example.com/slowmo#IsAboutPerformer"),
                Literal(int(performance_data_df["staff_number"].iloc[0])),
            )
        )
        response["candidates"] = utils.candidates_records(cool_new_super_graph)

    response.update(full_selected_message)

    return response


def set_preferences(req_info):
    preferences_utilities = req_info.get("Preferences", {}).get("Utilities", {})
    input_preferences: dict = preferences_utilities.get("Message_Format", {})
    individual_preferences: dict = {}
    for key in input_preferences:
        individual_preferences[key.lower()] = float(input_preferences[key])

    preferences: dict = default_preferences.copy()
    preferences.update(individual_preferences)

    min_value = min(preferences.values())
    max_value = max(preferences.values())

    for key in preferences:
        preferences[key] = (preferences[key] - min_value) / (max_value - min_value)

    display_format = None
    for key, value in preferences_utilities.get("Display_Format", {}).items():
        if value == 1 and key != "System-generated":
            display_format = key.lower()

    return {"Message_Format": preferences, "Display_Format": display_format}


def debug_output_if_set(graph: Graph, file_location):
    if settings.outputs is True and logger.at_least("DEBUG"):
        file_path = Path(file_location)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        graph.serialize(destination=file_path, format="json-ld", indent=2)
