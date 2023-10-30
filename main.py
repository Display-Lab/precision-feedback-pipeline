from fastapi import FastAPI, Request
from pydantic import BaseSettings
from rdflib import Graph, ConjunctiveGraph, Namespace, URIRef, RDFS, Literal
import pandas as pd
from graph_operations import read_graph, create_performer_graph
from bit_stomach.bit_stomach import Bit_stomach
from candidatesmasher.candidatesmasher import CandidateSmasher
from thinkpudding.thinkpudding import Thinkpudding
from esteemer.esteemer import Esteemer
from pictoralist.pictoralist import Pictoralist
import json
import webbrowser
import requests
from requests_file import FileAdapter
from io import BytesIO
import os
from dotenv import load_dotenv


global templates, pathways, measures
load_dotenv()
class Settings(BaseSettings):
    # Set values to env var, when undeclared default to PFKB repo
    templates: str = os.environ.get('templates',    'https://api.github.com/repos/Display-Lab/knowledge-base/contents/message_templates')
    pathways: str = os.environ.get('pathways',      'https://api.github.com/repos/Display-Lab/knowledge-base/contents/causal_pathways')
    measures: str = os.environ.get('measures',      'https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/measures.json')
    mpm: str =os.environ.get('mpm',      'https://raw.githubusercontent.com/Display-Lab/knowledge-base/main/motivational_potential_model.csv')
settings = Settings()   # Instance the class now for use below


### Create RDFlib graph from locally saved json files
def local_to_graph(thisDirectory, thisGraph):
    # Scrape directory, filter to only JSON files, build list of paths to the files (V2)
    print(f'Starting dir-to-list transform...')
    json_only = [entry.path for entry in os.scandir(thisDirectory) if entry.name.endswith('.json')]

    # Iterate through list, parsing list information into RDFlib graph object
    print(f'Starting graphing process...')
    for n in range(len(thisList)):
        temp_graph = Graph()                            # Creates empty RDFlib graph
        temp_graph.parse(thisList[n], format='json-ld') # Parse list data in JSON format
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
print("Starting session handler...")
se = requests.Session()
print(se)
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
    print(type(mpm))
    mpm_df=pd.read_csv(BytesIO(mpm))
    # print(df1)
    performer_graph=create_performer_graph(measure_details)
    
    #BitStomach
    bs=Bit_stomach(performer_graph,performance_data_df)
    BS=bs.annotate()
    op=BS.serialize(format='json-ld', indent=4)
    
    #CandidateSmasher
    cs=CandidateSmasher(BS,templates)
    df_graph=cs.get_graph_type()
    df_template=cs.get_template_data()
 
    CS=cs.create_candidates(df_graph,df_template)
    
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
  
    # selected_message=es.get_selected_message()
    
    
    # # # print(selected_message)
    if selected_message["text"]!= "No message selected":
    # # #Runnning Pictoralist

        ## Set init flag for image generation based on value of env var
        generate_image = not (os.environ.get("pictoraless") == "true")
        pc=Pictoralist(selected_message, p_df, generate_image, performance_data_df)
        ## Process env var declaration (must be string) to determine if image generation happens
        base64_image=pc.create_graph()
        selected_message["image"]=base64_image
        selected_message1=pc.prepare_selected_message()

    # '<img align="left" src="data:image/png;base64,%s">' %base64_image
    # ES=spek_es.serialize(format='json-ld', indent=4)
    # if str(debug)=="yes":
    #     f = open("outputs/spek_es.json", "w")
    #     f.write(ES)
    #     f.close()
    # print(vignette)
    
    return selected_message1
