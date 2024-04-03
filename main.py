import json
import os
import sys
import webbrowser
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Request
from loguru import logger
from rdflib import (  #, ConjunctiveGraph, Namespace, URIRef, RDFS, Literal
    BNode,
    Graph,
    Literal,
    URIRef,
    RDF
)
from rdflib.resource import Resource
from requests_file import FileAdapter

from bit_stomach.bit_stomach import BitStomach
from bitstomach2 import bitstomach
from candidatesmasher.candidatesmasher import CandidateSmasher
from esteemer import esteemer, utils
from pictoralist.pictoralist import Pictoralist
from thinkpudding.thinkpudding import Thinkpudding
from utils.graph_operations import create_performer_graph, read_graph
from utils.settings import settings
from candidate_pudding import candidate_pudding

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
        global measure_details, causal_pathways, templates, f3json, f5json, comparators

        f3json = se.get(settings.measures).text
        f5json = se.get(settings.mpm).content
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
    selected_message = {}
    req_info = await info.json()
    req_info1 = req_info
    performance_data = req_info1["Performance_data"]

    performance_data_df = pd.DataFrame(
        performance_data,
        columns=[
            "staff_number",
            "Measure_Name",
            "Month",
            "Passed_Count",
            "Flagged_Count",
            "Denominator",
            "peer_average_comparator",
            "peer_90th_percentile_benchmark",
            "peer_75th_percentile_benchmark",
            "MPOG_goal",
        ],
    )
    performance_data_df.columns = performance_data_df.iloc[0]
    performance_data_df = performance_data_df[1:]
    p_df = req_info1["Performance_data"]
    del req_info1["Performance_data"]
    history: dict = req_info1.setdefault("History",{})
    del req_info1["History"]  
    preferences = req_info1["Preferences"]
    ## Pass message instance ID from input message through to pictoralist
    message_instance_id = req_info1.get("message_instance_id")
    del req_info1["Preferences"]
    input_message = read_graph(req_info1)
    measure_details = Graph()

    for s, p, o in measure_details.triples((None, None, None)):
        measure_details.remove((s, p, o))

    measure_details = read_graph(f3json)
    mpm = f5json
    # print(type(mpm))
    mpm_df = pd.read_csv(BytesIO(mpm))
    # print(df1)
    performer_graph = create_performer_graph(measure_details)

    # BitStomach
    logger.info("Calling BitStomach from main...")

    # # Trying another strategy for graceful exit:
    # try:
    #     bs = BitStomach(performer_graph, performance_data_df)
    # except ValueError:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Insufficient significant data found for providing feedback, process aborted. Message_instance_id: {message_instance_id}",
    #         headers={"400-Error": "Invalid Input Error"},
    #     )
    #     sys.exit(4)

    # performer_graph = bs.annotate()
    # debug_output_if_set(performer_graph, "outputs/spek_bs.json")
    
    ### Start with cool new super graph
    
    cool_new_super_graph = Graph()
    comparators_graph = read_graph(comparators)
    cool_new_super_graph += comparators_graph    
    cool_new_super_graph += causal_pathways
    cool_new_super_graph += measure_details
    cool_new_super_graph += templates
    debug_output_if_set(cool_new_super_graph, "outputs/base.json")

    # BitStomach 2
    g: Graph = bitstomach.extract_signals(performance_data)
    performer_graph += g
    cool_new_super_graph += g
    debug_output_if_set(performer_graph, "outputs/spek_bs2.json")

    if settings.candidate_pudding:
        candidate_pudding.create_candidates(cool_new_super_graph)
    else:
        logger.info("CandidateSmasher and Thinkpuddung")
        #CandidateSmasher     
        logger.info("Calling CandidateSmasher from main...")
        cs = CandidateSmasher(performer_graph, templates)
        df_graph, goal_types, peer_types, top_10_types, top_25_types = cs.get_graph_type()
        df_template, df_1, df_2, df_3, df16 = cs.get_template_data()
        # create top_10
        CS = cs.create_candidates(top_10_types, df_1)
        # #create top_25
        CS = cs.create_candidates(top_25_types, df_2)
        # #creat peers
        CS = cs.create_candidates(peer_types, df_3)
        # create goal
        CS = cs.create_candidates(goal_types, df16)
        
        debug_output_if_set(performer_graph, "outputs/spek_cs.json")

        # Thinkpuddung
        logger.info("Calling ThinkPudding from main...")
        tp = Thinkpudding(CS, causal_pathways)
        tp.process_causalpathways()
        tp.process_performer_graph()
        tp.matching()
        performer_graph = tp.insert()
        debug_output_if_set(performer_graph, "outputs/spek_tp.json")

    # #Esteemer
    logger.info("Calling Esteemer from main...")

    for measure in utils.measures(cool_new_super_graph):
        candidates = utils.candidates(
            cool_new_super_graph, filter_acceptable=True, measure=measure
        )
        for candidate in candidates:
            # temporary shim to get candidates from existing thinkpudding into new graph
            #cool_new_super_candidate = add_candidate_to_super_graph(cool_new_super_graph, candidate)
            esteemer.score(candidate, history, preferences)
    selected_candidate = esteemer.select_candidate(cool_new_super_graph)

    # print updated graph by esteemer
    debug_output_if_set(performer_graph, "outputs/spek_st.json")

    selected_message = utils.render(cool_new_super_graph, selected_candidate)

    ### Pictoralist 2, now on the Nintendo DS: ###
    logger.info("Calling Pictoralist from main...")
    if selected_message["message_text"] != "No message selected":
        ## Initialize and run message and display generation:
        pc = Pictoralist(
            performance_data_df, p_df, selected_message, settings, message_instance_id
        )
        pc.prep_data_for_graphing()  # Setup dataframe of one measure, cleaned for graphing
        pc.fill_missing_months()  # Fill holes in dataframe where they exist
        pc.set_timeframe()  # Ensure no less than three months being graphed
        pc.finalize_text()  # Finalize text message and labels
        pc.graph_controller()  # Select and run graphing based on display type
        full_selected_message = pc.prepare_selected_message()
        if settings.log_level == "DEBUG":
            cool_new_super_graph.add((BNode("p1"),URIRef("http://example.com/slowmo#IsAboutPerformer"),Literal(performance_data_df["staff_number"].iloc[0])  ))
        
            full_selected_message["candidates"] = utils.candidates_records(cool_new_super_graph)
    else: 
        return selected_message
    return full_selected_message

def debug_output_if_set(performer_graph: Graph, file_location):
    if settings.outputs is True and settings.log_level == "DEBUG":
        file_path = Path(file_location)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        performer_graph.serialize(destination=file_path, format="json-ld", indent=2)

def add_candidate_to_super_graph(cool_new_super_graph: Graph, candidate: Resource) -> Resource:
    cool_new_super_candidate = cool_new_super_graph.resource(candidate.identifier)
    for p,o in candidate.predicate_objects():
        cool_new_super_candidate.add(p.identifier,o)   
    
    return cool_new_super_candidate

