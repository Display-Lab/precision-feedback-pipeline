from rdflib import Graph, ConjunctiveGraph, Namespace, URIRef, RDFS, Literal
from candidatesmasher.candidatesmasher import CandidateSmasher
from graph_operations import read_graph, create_performer_graph
from thinkpudding.thinkpudding import Thinkpudding
from bit_stomach.bit_stomach import Bit_stomach
from pictoralist.pictoralist import Pictoralist
from esteemer.esteemer import Esteemer
from requests_file import FileAdapter
from fastapi import FastAPI, Request
from pydantic import BaseSettings
from dotenv import dotenv_values
from io import BytesIO
import pandas as pd
import webbrowser
import requests
import logging
import json
import os

global templates, pathways, measures
config = {
    **dotenv_values(".env.local")        # Loads local testing environment file
    **dotenv_values(".env.remote")      # Loads remote env file for production (comment line out for local testing)
    **os.environ                            # Overwrite with env vars if set some other fashion
}
# Not yet finished with this, need to find a way to select between which config set to pull through to basesettings
class Settings(BaseSettings):
    # Knowledge to load on startup:                 Reads env vars first, then from env file the following keys:
    templates: str = os.environ.get('templates',    config['templates'])
    pathways: str = os.environ.get('pathways',      config['pathways'])
    measures: str = os.environ.get('measures',      config['measures'])
    mpm: str = os.environ.get('mpm',                config['mpm'])

    # Configuration settings (currently work-arounded... exploring better setup with decouple)
    log_level:      str = os.environ.get('log_level',               config['INFO'])              # Logging level of pipeline instance (info, debug)
    display_window: int = int(os.environ.get('display_window',      config['display_window']))   # Months to show in display
    pictoraless:   bool = bool(int(os.environ.get('pictoraless',    config['pictoraless'])))     # Prevent image generation when true
    goal_line:     bool = bool(int(os.environ.get('plot_goal_line', config['plot_goal_line'])))  # Plots goal line in image if true
settings = Settings()


### Create RDFlib graph from locally saved json files
def local_to_graph(thisDirectory, thisGraph):
    # Scrape directory, filter to only JSON files, build list of paths to the files (V2)
    print(f'Starting dir-to-list transform...')
    json_only = [entry.path for entry in os.scandir(thisDirectory) if entry.name.endswith('.json')]
    ## inject logging statement (Info lvl) here to track what files loaded visually for testers

    # Iterate through list, parsing list information into RDFlib graph object
    print(f'Starting graphing process...')
    for n in range(len(json_only)):
        temp_graph = Graph()                            # Creates empty RDFlib graph
        temp_graph.parse(json_only[n], format='json-ld') # Parse list data in JSON format
        thisGraph = thisGraph + temp_graph              # Add parsed data to graph object
    return thisGraph


### Create RDFlib graph from remote knowledgebase JSON files
def remote_to_graph(contentURL, thisGraph):
    # Fetch JSON content from URL (directory)
    response = requests.get(contentURL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch JSON content from URL: {contentURL}")
    
    try:
        contents = response.json()
        for item in contents:
            file_name = item["name"]
            if file_name.endswith(".json"):  # Check if the file has a .json extension
                file_jsoned = json.loads(requests.get(item["download_url"]).content)        # Download content, store as JSON
                temp_graph = Graph().parse(data=json.dumps(file_jsoned), format='json-ld')  # Parse JSON, store as graph
                print(f'Graphed file {file_name}')
                thisGraph += temp_graph
            else:
                print(f"Skipped non-JSON file: {file_name}")
    except json.JSONDecodeError as e:
        raise Exception("Failed parsing JSON content.")
        
    return thisGraph


### Create empty RDFlib graphs to store resource description triples
pathway_graph   = Graph()
template_graph  = Graph()

### Changes loading strategy depending on the source of PFKB content
if not settings.pathways.startswith('http'):
    # Build graphs with local os.dirname method if using file URI
    causal_pathways = local_to_graph(settings.pathways, pathway_graph)
    templates       = local_to_graph(settings.templates, template_graph)
else:
    # Build graphs from remote resource if using URLs
    causal_pathways = remote_to_graph(settings.pathways, pathway_graph)
    templates       = remote_to_graph(settings.templates, template_graph)

# Set up request session as se, config to handle file URIs with FileAdapter
logging.info:("Starting session handler...")
se = requests.Session()
se.mount('file://',FileAdapter())
app = FastAPI()



@app.on_event("startup")
async def startup_event():
    try:
        global measure_details,causal_pathways,templates,f3json,f5json

        f3json=se.get(settings.measures).text
        f5json=se.get(settings.mpm).content
        causal_pathways = causal_pathways        
        templates =templates
        
    except Exception as e:
        print("Startup aborted, see traceback:")
        raise e
    


@app.get("/")
async def root():
    
    return{"Hello":"Universe"}



@app.get("/template/")
async def template():
    github_link ="https://raw.githubusercontent.com/Display-Lab/precision-feedback-pipeline/main/input_message.json"
    return webbrowser.open(github_link)



@app.post("/createprecisionfeedback/")
async def createprecisionfeedback(info:Request):
    selected_message={}
    req_info =await info.json()
    req_info1=req_info
    performance_data = req_info1["Performance_data"]
    
    performance_data_df =pd.DataFrame (performance_data, columns = [ "staff_number","Measure_Name","Month","Passed_Count","Flagged_Count","Denominator","peer_average_comparator","peer_90th_percentile_benchmark","peer_75th_percentile_benchmark","MPOG_goal"])
    performance_data_df.columns = performance_data_df.iloc[0]
    performance_data_df = performance_data_df[1:]
    p_df=req_info1["Performance_data"]
    del req_info1["Performance_data"]
    history=req_info1["History"]
    del req_info1["History"]
    preferences=req_info1["Preferences"]
    del req_info1["Preferences"]
    input_message=read_graph(req_info1)
    measure_details= Graph()
    
    for s,p,o in measure_details.triples((None,None,None)):
        measure_details.remove((s,p,o))
    
    measure_details=read_graph(f3json)
    mpm=f5json
    #print(type(mpm))
    mpm_df=pd.read_csv(BytesIO(mpm))
    # print(df1)
    performer_graph=create_performer_graph(measure_details)
    
    #BitStomach
    bs=Bit_stomach(performer_graph,performance_data_df)
    BS=bs.annotate()
    op=BS.serialize(format='json-ld', indent=4)
    
    
    #CandidateSmasher
    cs=CandidateSmasher(BS,templates)
    df_graph,goal_types,df_graph,top_10_types,top_25_types=cs.get_graph_type()
    df_template,df_1,df_2,df_3,df16=cs.get_template_data()
    #create top_10
    CS=cs.create_candidates(top_10_types,df_1)
    # #create top_25
    CS=cs.create_candidates(top_25_types,df_2)
    # #creat peers
    CS=cs.create_candidates(df_graph,df_3)
    #create goal
    CS=cs.create_candidates(goal_types,df16)
    
    #Thinkpuddung
    tp=Thinkpudding(CS,causal_pathways)
    tp.process_causalpathways()
    tp.process_spek()
    tp.matching()
    spek_tp=tp.insert()
    op=spek_tp.serialize(format='json-ld', indent=4)


    # #Esteemer
    measure_list=performance_data_df["measure"].drop_duplicates()
    # print(*measure_list)
    es=Esteemer(spek_tp,measure_list,preferences,history,mpm_df)
    # # es.apply_preferences()
    # # es.apply_history()
    es.process_spek()
    es.process_history()
    es.process_mpm()
    node,spek_es=es.score()
    # node,spek_es=es.select()
    selected_message=es.get_selected_message()
    # # es.apply_history()
    

    ### Pictoralist 2, now on the Nintendo DS: ###
    logging.debug('Starting Pictoralist...')
    if selected_message["message_text"]!= "No message selected":        
        ## Initialize and run message and display generation:
        pc=Pictoralist(performance_data_df, p_df, selected_message, settings)
        pc.prep_data_for_graphing()
        pc.fill_missing_months()
        pc.finalize_text()
        pc.set_timeframe()
        pc.graph_controller()
        full_selected_message   = pc.prepare_selected_message()
    
    return full_selected_message
