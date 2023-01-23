from http.client import HTTPException
from typing import List
from fastapi import FastAPI,Request
from uuid import UUID,uuid4
from rdflib import Graph, Literal, Namespace, URIRef
import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from graph_operations import read_graph, create_base_graph,create_performer_graph
#import bit_stomach.bit_stomach as bit_stomach
from bit_stomach.bit_stomach import Bit_stomach
from candidatesmasher.candidatesmasher import CandidateSmasher
from thinkpudding.thinkpudding import Thinkpudding
import json
app = FastAPI()

measure_details=Graph()
causal_pathways=Graph()
templates=Graph()
message_code=Graph()
@app.on_event("startup")
async def startup_event():
    try:
        
        f1=open("./startup/message_code.json")
        f2=open("./startup/causal_pathways.json")
        f3=open("./startup/measure_details.json")
        f4=open("./startup/templates.json")
        f1json=json.load(f1)
        f2json=json.load(f2)
        f3json=json.load(f3)
        f4json=json.load(f4)
        global measure_details,message_code,causal_pathways,templates
        message_code=read_graph(f1json)
        causal_pathways=read_graph(f2json)
        measure_details=read_graph(f3json)
        templates=read_graph(f4json)
        
        
        #base_graph=create_base_graph(message_code,causal_pathways,measure_details,templates)
        # df=to_dataframe(base_graph)
        # df.to_csv("basegraph.csv")
        print("startup is complete")
    except Exception as e:
        print("Looks like there is some problem in connection,see below traceback")
        raise e
@app.get("/")
async def root():
    return{"Hello":"Universe"}

@app.post("/createprecisionfeedback/")
async def createprecisionfeedback(info:Request):
    req_info =await info.json()
    req_info1=req_info
    performance_data = req_info1["Performance_data"]
    performance_data_df =pd.DataFrame (performance_data, columns = [ "Staff_Number","Measure_Name","Month","Passed_Count","Flagged_Count","Denominator","Peer_Average"])
    performance_data_df.columns = performance_data_df.iloc[0]
    performance_data_df = performance_data_df[1:]
    #df = df.iloc[1: , :]
    #performance_data_df.to_csv('pd.csv', index=False)
    #print(type())
    del req_info1["Performance_data"]
    history=req_info1["History"]
    del req_info1["History"]
    preferences=req_info1["Preferences"]
    del req_info1["Preferences"]
    input_message=read_graph(req_info1)
    performer_graph=create_performer_graph(measure_details)
    #BitStomach
    bs=Bit_stomach(performer_graph,performance_data_df)
    BS=bs.annotate()
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

    
    TP=performer_graph.serialize(format='json-ld', indent=4)
    f = open("TP.json", "w")
    f.write(TP)
    f.close()
    
    return {
        "status":"Success",
         "data": TP
    }
    

