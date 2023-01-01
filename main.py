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
import json
app = FastAPI()

base_graph=Graph()

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
        message_code=read_graph(f1json)
        causal_pathways=read_graph(f2json)
        measure_details=read_graph(f3json)
        templates=read_graph(f4json)
        
        global base_graph
        base_graph=create_base_graph(message_code,causal_pathways,measure_details,templates)
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
    req_info1 =await info.json()
    input_message=read_graph(req_info1)
    performer_graph=create_performer_graph(input_message,base_graph)
    a=performer_graph.serialize(format='json-ld', indent=4)
    
    return {
        "status":"Success",
        "data": a
    }
    

