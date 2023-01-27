import json
import sys
import warnings
import time
import logging
import json
import random
#from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe



# from .load_for_real import load
# from load import read, transform,read_contenders,read_measures,read_comparators
# from score import score, select,apply_indv_preferences,apply_history_message

# load()

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
# Read graph and convert to dataframe
start_time = time.time()
class Esteemer():
    def __init__(self, spek_tp, preferences, message_code, history):
        self.y=[]
        self.spek_tp=spek_tp
        s=URIRef("http://example.com/app#display-lab")
        p=URIRef("http://example.com/slowmo#HasCandidate")
        p1=URIRef("slowmo:acceptable_by")
        
        for s,p,o in self.spek_tp.triples( (s, p, None) ):
            s1= o
            for s,p,o in self.spek_tp.triples((s1,p1,None)):
                self.y.append(s)
        self.node=random.choice(self.y)
        self.message_code=message_code
    def select(self):
        o2=URIRef("http://example.com/slowmo#selected")
        self.spek_tp.add((self.node,RDF.type,o2))
        return self.node,self.spek_tp
    def get_selected_message(self):
        s_m={}
        s=self.node
        p=URIRef("psdo:PerformanceSummaryDisplay")
        p2=URIRef("name")
        p3=URIRef("psdo:PerformanceSummaryTextualEntity")
        for s1,p1,o1 in self.spek_tp.triples((s,p,None)):
            #print(o1)
            s_m["display"]=o1
        for s1,p1,o1 in self.spek_tp.triples((s,p2,None)):
            #print(o1)
            s_m["name"]=o1
        for s1,p3,o1 in self.spek_tp.triples((s,p3,None)):
            #print(o1)
            s_m["text"]=o1
        return s_m



    


    

            

                
        

# meaningful_messages_final = transform(contenders_graph,measures_graph,comparator_graph,measure_list)

# start_time1 = time.time()
# meaningful_messages_final = score(meaningful_messages_final)


# applied_individual_messages,max_val = apply_indv_preferences(meaningful_messages_final,indv_preferences_read)
# val = max_val.split('_')

# applied_history_filter = apply_history_message(applied_individual_messages,history,val[0],message_code)




# finalData = select(applied_history_filter,val[0],message_code)



# logging.critical("--score and select %s seconds ---" % (time.time() - start_time1))
# print(finalData)

# time_taken = time.time()-start_time
logging.critical("---total esteemer run time according python script %s seconds ---" % (time.time() - start_time))

"""with open('data.json', 'a') as f:
    f.write(finalData + '\n')"""
