

import warnings
import time
import logging

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe


warnings.filterwarnings("ignore")


def read_graph(file):
    start_time = time.time()
    g = Graph()
    g.parse(data=file,
            format='json-ld')
    
    logging.critical(" reading graph--- %s seconds ---" % (time.time() - start_time)) 
    return g

def create_base_graph(g1,g2,g3,g4):
    base_graph=g1+g2+g3+g4 #merging graphs
    return base_graph
def create_performer_graph(g2):
    performer_graph=g2
    return performer_graph
