import json
import sys
import warnings
import time
import logging
import json
#from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper
import collections

from thinkpudding.load import read,process_causalpathways,process_spek,matching
from thinkpudding.insert import insert
class Thinkpudding:
    start_time1 = time.time()
    spek_out_dicts = {}
    caus_out_dict={}
    final_dict={}
    
    def __init__(self, spek_cs, causal_pathways):
        start_time = time.time()
        #self.spek_cs1 = json.dumps(spek_cs)
        self.spek_cs=spek_cs
        logging.critical(" reading spek graph--- %s seconds ---" % (time.time() - start_time)) 
        start_time = time.time()
        #self.causal_pathways1 = json.dumps(causal_pathways)
        self.causal_pathways=causal_pathways
        logging.critical(" reading causal pathways graph--- %s seconds ---" % (time.time() - start_time))
    
    def process_causalpathways(self):
        start_time = time.time()
        self.caus_out_dict=process_causalpathways(self.causal_pathways)
        logging.critical(" processing causal pathways--- %s seconds ---" % (time.time() - start_time))

    def process_spek(self):
        start_time = time.time()
        self.spek_out_dicts=process_spek(self.spek_cs)
        logging.critical(" processing spek_cs--- %s seconds ---" % (time.time() - start_time))
    
    def matching(self):
        start_time = time.time()
        self.merged_list=matching(self.caus_out_dict,self.spek_out_dicts)
        logging.critical(" processing matching--- %s seconds ---" % (time.time() - start_time))

    def insert(self):
        start_time = time.time()
        self.spek_tp=insert(self.merged_list,self.spek_cs)
        logging.critical(" inserting acceptable by--- %s seconds ---" % (time.time() - start_time))
        return self.spek_tp

# print(spek_tp.serialize(format='json-ld', indent=4))   
# logging.critical("complete thinkpudding--- %s seconds ---" % (time.time() - start_time1))
#print(caus_out_dict) 
#print(spek_out_dicts) 
#print(final_dict)          

