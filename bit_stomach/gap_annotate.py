import sys
import warnings
import time
import logging
import json
import re
import numpy as np 
import matplotlib.pyplot as plt 

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper
#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector

s=URIRef("http://example.com/app#display-lab")
p=URIRef('http://example.com/slowmo#IsAboutMeasure')



def goal_gap_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    #a=insert_annotate(input_graph)
    
    gap_size=latest_measure_df['goal_comparison_value']-latest_measure_df['Performance_Rate']
    
    if (gap_size[0]!= 0):
        ac=BNode(latest_measure_df["Measure_Name"][0])
        av=comparator_bnode
        goal_gap_size=gap_size[0]
        goal_gap_size=Literal(goal_gap_size)
    #         #annotate goal comparator
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        input_graph=annotate_goal_comparator(input_graph,o14,ac,av)
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        input_graph=annotate_performance_goal_gap(input_graph,o14,ac,av)
        if(gap_size[0]>0):
            o14=BNode() 
            input_graph.add((s14,p14,o14))
            input_graph=annotate_positive_goal_gap(input_graph,o14,ac,av,goal_gap_size)

        if(gap_size[0]<0):
            o14=BNode() 
            input_graph.add((s14,p14,o14))
            input_graph=annotate_negative_goal_gap(input_graph,o14,ac,av,goal_gap_size)
        

    

    return input_graph

def annotate_goal_comparator(a,s16,measure_Name,o16):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000094')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    return a

def annotate_performance_goal_gap(a,s16,measure_Name,o16):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000106')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    return a

def annotate_positive_goal_gap(a,s16,measure_Name,o16,goal_gap_size):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000104')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    p18=URIRef('http://example.com/slowmo#PerformanceGapSize')
    o18=goal_gap_size
    a.add((s16,p18,o18))
    return a

def annotate_negative_goal_gap(a,s16,measure_Name,o16,goal_gap_size):

    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000105')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    p18=URIRef('http://example.com/slowmo#PerformanceGapSize')
    o18=goal_gap_size
    a.add((s16,p18,o18))
    return a

def peer_gap_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    #a=insert_annotate(input_graph)
    
    gap_size=latest_measure_df['Peer_Average']-latest_measure_df['Performance_Rate']
    
    if (gap_size[0]!= 0):
        ac=BNode(latest_measure_df["Measure_Name"][0])
        av=comparator_bnode
        goal_gap_size=gap_size[0]
        goal_gap_size=Literal(goal_gap_size)
    #         #annotate goal comparator
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        input_graph=annotate_peer_comparator(input_graph,o14,ac,av)
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        input_graph=annotate_performance_peer_gap(input_graph,o14,ac,av)
        if(gap_size[0]>0):
            o14=BNode() 
            input_graph.add((s14,p14,o14))
            input_graph=annotate_positive_peer_gap(input_graph,o14,ac,av,goal_gap_size)
        if(gap_size[0]<0):
            o14=BNode() 
            input_graph.add((s14,p14,o14))
            input_graph=annotate_negative_peer_gap(input_graph,o14,ac,av,goal_gap_size)
        

    

    return input_graph

def annotate_peer_comparator(a,s16,measure_Name,o16):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000095')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    return a

def annotate_performance_peer_gap(a,s16,measure_Name,o16):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000106')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    return a

def annotate_positive_peer_gap(a,s16,measure_Name,o16,goal_gap_size):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000104')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    p18=URIRef('http://example.com/slowmo#PerformanceGapSize')
    o18=goal_gap_size
    a.add((s16,p18,o18))
    return a

def annotate_negative_peer_gap(a,s16,measure_Name,o16,goal_gap_size):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000105')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    p18=URIRef('http://example.com/slowmo#PerformanceGapSize')
    o18=goal_gap_size
    a.add((s16,p18,o18))
    return a