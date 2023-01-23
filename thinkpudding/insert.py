import warnings
import time
import logging

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

def insert(merged_list,spek_cs):
    p=URIRef("slowmo:acceptable_by")
    for x in merged_list:
        for z in x[0]:
            o=z
            for i in x[1]:
                s=i
                spek_cs.add((s, p, o,))


    
   
    # for key, value in final_dict.items():
    #     print(list(key))
    #print(value)
        # for i in value:
        #     s=i
        #     o=[key]
        #     spek_cs.add((s, p, o,))
    return spek_cs
