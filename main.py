from fastapi import FastAPI,Request
from pydantic import BaseSettings
from rdflib import Graph,ConjunctiveGraph ,Namespace,URIRef,RDFS,Literal
import pandas as pd
from rdflib import Graph
from graph_operations import read_graph, create_performer_graph
#import bit_stomach.bit_stomach as bit_stomach
from bit_stomach.bit_stomach import Bit_stomach
from candidatesmasher.candidatesmasher import CandidateSmasher
from thinkpudding.thinkpudding import Thinkpudding
from esteemer.esteemer import Esteemer
from pictoralist.pictoralist import Pictoralist
import json
import requests
from requests_file import FileAdapter


import os

class Settings(BaseSettings):
    global pathways,templates
    pathways = os.path.dirname("startup/causal_pathways/")
    #pathways: str = "file://"+os.path.abspath("startup/social_loss.json")
    measures: str ="file://"+os.path.abspath("startup/measures.json")
    templates =os.path.dirname("startup/templates/")
    #templates: str ="file://"+os.path.abspath("startup/templates.json")
    # des=templates
    asa=[]

asa=os.listdir(pathways)
asaa=os.listdir(templates)
list2 = (pathways+"/"+pd.Series(asa)).tolist()

list3 = (templates+"/"+pd.Series(asaa)).tolist()

graph = Graph()
graph1=Graph()

for sd in range(len(list2)):
    adf="g"+str(sd)
    adf=Graph()
    adf.parse(list2[sd])
    graph = graph + adf
for sdf in range(len(list3)):
    adfs="g"+str(sdf)
    adfs=Graph()
    adfs.parse(list3[sdf])
    graph1 = graph1 + adfs

measure_details=Graph()
causal_pathways=graph
templates=graph1


se =requests.Session()
se.mount('file://',FileAdapter())
settings = Settings()
app = FastAPI()





@app.on_event("startup")
async def startup_event():
    try:
        
      
        global measure_details,causal_pathways,templates,f3json
        
        
        #f2json=se.get(settings.pathways).text
        f3json=se.get(settings.measures).text
        #f4json=se.get(settings.templates).text
       
        causal_pathways = causal_pathways
        # causal_pathways=read_graph(f2json)
        
        templates =templates
       # templates=read_graph(f4json)
        print("startup is complete")
    except Exception as e:
        print("Looks like there is some problem in connection,see below traceback")
        raise e
    

@app.get("/")
async def root():
    return{"Hello":"Universe"}
@app.get("/template/")
async def template():
    f = open('startup/input_message_demo.json')
    data = json.load(f)
    
    return data

@app.post("/createprecisionfeedback/")
async def createprecisionfeedback(info:Request):
    selected_message={}
    req_info =await info.json()
    req_info1=req_info
    performance_data = req_info1["Performance_data"]
    debug=req_info1["debug"]
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
    performer_graph=create_performer_graph(measure_details)
    
    #BitStomach
    bs=Bit_stomach(performer_graph,performance_data_df)
    BS=bs.annotate()
    op=BS.serialize(format='json-ld', indent=4)
    if str(debug)=="yes":
        f = open("outputs/spek_bs.json", "w")
        f.write(op)
        f.close()
    
    #CandidateSmasher
    cs=CandidateSmasher(BS,templates)
    df_graph=cs.get_graph_type()
    df_template=cs.get_template_data()
 
    CS=cs.create_candidates(df_graph,df_template)
    if str(debug)=="yes":
        op=CS.serialize(format='json-ld', indent=4)
        f = open("outputs/spek_cs.json", "w")
        f.write(op)
        f.close()
    #Thinkpuddung
    tp=Thinkpudding(CS,causal_pathways)
    tp.process_causalpathways()
    tp.process_spek()
    tp.matching()
    spek_tp=tp.insert()
    op=spek_tp.serialize(format='json-ld', indent=4)
    if str(debug)=="yes":
        op=spek_tp.serialize(format='json-ld', indent=4)
        f = open("outputs/spek_tp.json", "w")
        f.write(op)
        f.close()

    # #Esteemer
    es=Esteemer(spek_tp,preferences,history)
    
    # # es.apply_preferences()
    # # es.apply_history()
    node,spek_es=es.select()
    selected_message=es.get_selected_message()
    # # es.apply_history()
  
    selected_message=es.get_selected_message()
    
    
    # # print(selected_message)
    if selected_message["text"]!= "No message selected":
    # # #Runnning Pictoralist
        pc=Pictoralist(selected_message,p_df,performance_data_df)
        base64_image=pc.create_graph()
        selected_message["image"]=base64_image
        
        selected_message1=pc.prepare_selected_message()
    # '<img align="left" src="data:image/png;base64,%s">' %base64_image
    ES=spek_es.serialize(format='json-ld', indent=4)
    if str(debug)=="yes":
        f = open("outputs/spek_es.json", "w")
        f.write(ES)
        f.close()
    # print(vignette)
    
    return selected_message1
        # "location":settings.location
       
        # "selected_message": selected_message
        #   "selected_message": selected_message
    
    

