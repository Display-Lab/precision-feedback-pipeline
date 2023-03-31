from fastapi import FastAPI,Request
from rdflib import Graph
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
app = FastAPI()

measure_details=Graph()
causal_pathways=Graph()
templates=Graph()
message_code=Graph()
causal_pathways_alice=Graph()
templates_alice=Graph()

@app.on_event("startup")
async def startup_event():
    try:
        
        f1=open("./startup/message_code.json")
        f2=open("./startup/causal_pathways.json")
        f3=open("./startup/measure_details.json")
        f4=open("./startup/templates.json")
        # f5=open("./startup/causal_pathways_alice.json")
        # f6=open("./startup/templates_alice.json")
        global measure_details,message_code,causal_pathways,templates,templates_alice,causal_pathways_alice,f3json
        f1json=json.load(f1)
        f2json=json.load(f2)
        f3json=json.load(f3)
        f4json=json.load(f4)
        # f5json=json.load(f5)
        # f6json=json.load(f6)
        
        message_code=read_graph(f1json)
        causal_pathways=read_graph(f2json)
        global templates
        templates=read_graph(f4json)
        # causal_pathways_alice=read_graph(f5json)
        # templates_alice=read_graph(f6json)
        
        
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
    selected_message={}
    req_info =await info.json()
    req_info1=req_info
    performance_data = req_info1["Performance_data"]
    vignette=req_info1["vignette"]
    debug=req_info1["debug"]
    performance_data_df =pd.DataFrame (performance_data, columns = [ "Staff_Number","Measure_Name","Month","Passed_Count","Flagged_Count","Denominator","Peer_Average","Top_10_Average","Top_25_Average"])
    performance_data_df.columns = performance_data_df.iloc[0]
    performance_data_df = performance_data_df[1:]
    #df = df.iloc[1: , :]
    #performance_data_df.to_csv('pd.csv', index=False)
    #print(type())
    if str(vignette)!="base":
        csp="./startup/"+str(vignette)+"/causal_pathways.json"
        temp="./startup/"+str(vignette)+"/templates.json"
        f2=open(csp)
        f4=open(temp)
        f2json=json.load(f2)
        f4json=json.load(f4)
        causal_pathways=read_graph(f2json)
        templates=read_graph(f4json)
    else:
        f2=open("./startup/causal_pathways.json")
        f4=open("./startup/templates.json")
        f2json=json.load(f2)
        f4json=json.load(f4)
        causal_pathways=read_graph(f2json)
        templates=read_graph(f4json)

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
    # # # es.apply_history()
  
    # selected_message=es.get_selected_message()
    # for k,v in selected_message.items():
    #     print(k,v)
    
    # # print(selected_message)
    if selected_message["text"]!= "No message selected":
    # #Runnning Pictoralist
        pc=Pictoralist(selected_message,performance_data_df)
        base64_image=pc.create_graph()
        selected_message["image"]=base64_image
    # # '<img align="left" src="data:image/png;base64,%s">' %base64_image
    ES=spek_es.serialize(format='json-ld', indent=4)
    if str(debug)=="yes":
        f = open("outputs/spek_es.json", "w")
        f.write(ES)
        f.close()
    # print(vignette)
    
    return {
        "status":"Success",
        "selected_message": selected_message
        #   "selected_message": selected_message
    }
    

