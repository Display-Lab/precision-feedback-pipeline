import json
import os
import sys
import webbrowser
from pathlib import Path

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
from utils.namespace import PSDO
from utils.settings import settings

global templates, pathways, measures, comparators

### Logging module setup (using loguru module)
logger.remove()
logger.add(
    sys.stdout, colorize=True, format="{level}|  {message}", level=settings.log_level
)

## Log of instance configuration
logger.info("Startup configuration for this instance:")
for attribute in dir(settings):
    if not attribute.startswith("__"):
        value = getattr(settings, attribute)
        logger.info(f"{attribute}:\t{value}")


### Create RDFlib graph from locally saved json files
def local_to_graph(thisDirectory, thisGraph):
    logger.debug("Starting function local_to_graph...")

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
        thisGraph = thisGraph + temp_graph  # Add parsed data to graph object
    return thisGraph


### Create RDFlib graph from remote knowledgebase JSON files
def remote_to_graph(contentURL, thisGraph):
    logger.debug("Starting function remote_to_graph...")

    # Fetch JSON content from URL (directory)
    response = requests.get(contentURL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch JSON content from URL: {contentURL}")

    try:
        contents = response.json()
        for item in contents:
            file_name = item["name"]
            if file_name.endswith(".json"):  # Check if the file has a .json extension
                file_jsoned = json.loads(
                    requests.get(item["download_url"]).content
                )  # Download content, store as JSON
                temp_graph = Graph().parse(
                    data=json.dumps(file_jsoned), format="json-ld"
                )  # Parse JSON, store as graph
                logger.debug(f"Graphed file {file_name}")
                thisGraph += temp_graph

    except json.JSONDecodeError:
        raise Exception("Failed parsing JSON content.")

    return thisGraph


### Create empty RDFlib graphs to store resource description triples
pathway_graph = Graph()
template_graph = Graph()

### Changes loading strategy depending on the source of PFKB content
if not settings.pathways.startswith("http"):
    # Build graphs with local os.dirname method if using file URI
    causal_pathways = local_to_graph(settings.pathways, pathway_graph)
    templates = local_to_graph(settings.templates, template_graph)
else:
    # Build graphs from remote resource if using URLs
    causal_pathways = remote_to_graph(settings.pathways, pathway_graph)
    templates = remote_to_graph(settings.templates, template_graph)

# Set up request session as se, config to handle file URIs with FileAdapter
se = requests.Session()
se.mount("file://", FileAdapter())
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    try:
        global measure_details, causal_pathways, templates, f3json, comparators

        f3json = se.get(settings.measures).text
        causal_pathways = causal_pathways
        templates = templates
        comparators = se.get(settings.comparators).text

    except Exception as e:
        print("Startup aborted, see traceback:")
        raise e


@app.get("/")
async def root():
    return {"Hello": "Universe"}


@app.get("/template/")
async def template():
    github_link = "https://raw.githubusercontent.com/Display-Lab/precision-feedback-pipeline/main/input_message.json"
    return webbrowser.open(github_link)


@app.post("/createprecisionfeedback/")
async def createprecisionfeedback(info: Request):
    req_info = await info.json()

    performance_data_df = bitstomach.fix_up(req_info)

    history: dict = req_info.get("History", {})

    input_preferences: dict = (
        req_info.get("Preferences", {}).get("Utilities", {}).get("Message_Format", {})
    )
    preferences = {
        "Social gain": "1.007650319",
        "Social stayed better": "0.4786461911",
        "Worsening": "-1.7261141",
        "Improving": "0.258245277",
        "Social loss": "0.7730646814",
        "Social stayed worse": "-0.5986969529",
        "Social better": "-0.1251083934",
        "Social worse": "-1.154453186",
        "Social approach": "1.086765623",
        "Goal gain": "1.007650319",
        "Goal approach": "1.086765623",
    }.copy()
    preferences.update(input_preferences)

    cool_new_super_graph = Graph()
    comparators_graph = read_graph(comparators)
    cool_new_super_graph += comparators_graph
    cool_new_super_graph += causal_pathways
    cool_new_super_graph += read_graph(f3json)
    cool_new_super_graph += templates
    debug_output_if_set(cool_new_super_graph, "outputs/base.json")

    # BitStomach
    logger.info("Calling BitStomach from main...")

    g: Graph = bitstomach.extract_signals(performance_data_df)
    performance_content = g.resource(BNode("performance_content"))
    if len(list(performance_content[PSDO.motivating_information])) == 0:
        cool_new_super_graph.close()
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient significant data found for providing feedback, process aborted. Message_instance_id: {req_info['message_instance_id']}",
            headers={"400-Error": "Invalid Input Error"},
        )

    cool_new_super_graph += g
    debug_output_if_set(cool_new_super_graph, "outputs/spek_bs.json")

    # candidate_pudding
    logger.info("Calling candidate_pudding from main...")
    candidate_pudding.create_candidates(cool_new_super_graph)

    # #Esteemer
    logger.info("Calling Esteemer from main...")

    for measure in cool_new_super_graph[: RDF.type : PSDO.performance_measure_content]:
        candidates = utils.candidates(
            cool_new_super_graph, filter_acceptable=True, measure=measure
        )
        for candidate in candidates:
            esteemer.score(candidate, history, preferences)
    selected_candidate = esteemer.select_candidate(cool_new_super_graph)

    # print updated graph by esteemer
    debug_output_if_set(cool_new_super_graph, "outputs/spek_st.json")

    selected_message = utils.render(cool_new_super_graph, selected_candidate)

    ### Pictoralist 2, now on the Nintendo DS: ###
    logger.info("Calling Pictoralist from main...")
    if selected_message["message_text"] != "No message selected":
        ## Initialize and run message and display generation:
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

    if settings.log_level == "DEBUG":
        cool_new_super_graph.add(
            (
                BNode("p1"),
                URIRef("http://example.com/slowmo#IsAboutPerformer"),
                Literal(performance_data_df["staff_number"].iloc[0]),
            )
        )

        full_selected_message["candidates"] = utils.candidates_records(
            cool_new_super_graph
        )

    cool_new_super_graph.close()
    return full_selected_message


def debug_output_if_set(graph: Graph, file_location):
    if settings.outputs is True and settings.log_level == "DEBUG":
        file_path = Path(file_location)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        graph.serialize(destination=file_path, format="json-ld", indent=2)
