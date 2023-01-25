import warnings
import time
import logging


import sys
import warnings
import time
import logging
import json
import re
import numpy as np 


import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector
#from insert_annotate import insert_annotate

from bit_stomach.prepare_data_annotate import Prepare_data_annotate

class Bit_stomach:
    def __init__(self,input_graph:Graph,performance_data:pd.DataFrame):
        self.measure_dicts={}
        self.goal_dicts={}
        self.goal_comparison_dicts={}
        self.performance_data_df=performance_data
        self.input_graph=input_graph
        s=URIRef("http://example.com/app#display-lab")
        p=URIRef('http://example.com/slowmo#IsAboutMeasure')
        p1=URIRef("http://example.com/slowmo#WithComparator")
        p3=URIRef('http://schema.org/name')
        o5=URIRef("http://purl.obolibrary.org/obo/psdo_0000095")
        p5=RDF.type
        p6=URIRef("http://example.com/slowmo#ComparisonValue")
        p21=URIRef("http://purl.org/dc/terms/title")
        p22=URIRef("http://schema.org/name")
        o21=Literal("PEERS")
        o22=Literal("peers") 
        self.input_graph=input_graph
        #insert blank nodes for social comparators for each measure
        for s,p,o in self.input_graph.triples((s, p, None)):
            s1=o
            o11=BNode()
            self.input_graph.add((s1,p1,o11))  
            s11=o11
            self.input_graph.add((s11,p5,o5))
            self.input_graph.add((s11,p21,o21))
            self.input_graph.add((s11,p22,o22))
        #get comparison values for goal from base graph and get Blank nodes for both goal and peer comparators
        for s,p,o in self.input_graph.triples((s, p, None)):
            s1=o
            for s2,p2,o2 in self.input_graph.triples((s1,p1,None)):
                self.measure_dicts[s1]=o2
                s3=o2
                for s4,p4,o4 in self.input_graph.triples((s3,p3,None)):
            # if str(o4)=="peers":
            #     #social_dicts[s1]=o2
            #     s5=s3
            #     #f.write(str(s5))
            #     # a.add((s5,p5,o5))
            #     for s7,p7,o7 in a.triples((s3,p6,None)):
            #         social_comparison_dicts[s1]=o7
                        if str(o4)=="goal":
                            self.goal_dicts[s1]=o2
                            for s8,p8,o8 in self.input_graph.triples((s3,p6,None)):
                                self.goal_comparison_dicts[s1]=o8

    def annotate(self):
        a=self.input_graph
        goaldf=pd.DataFrame(self.goal_comparison_dicts.items())
        
#socialdf=pd.DataFrame(social_comparison_dicts.items())
        goaldf1=pd.DataFrame(self.goal_comparison_dicts.items())
        goaldf1.columns =['Measure_Name', 'goal_comparison_value']
        
        pr=Prepare_data_annotate(a,self.performance_data_df,goaldf1)

        measure_list=[]
        self.performance_data_df["Measure_Name"]=self.performance_data_df["Measure_Name"].str.decode(encoding="UTF-8")

        measure_list=self.performance_data_df["Measure_Name"].drop_duplicates()
 
        for index, element in enumerate(measure_list):
            measure_name=element
            a=pr.gaol_gap_annotate(measure_name,**self.goal_dicts)
            a=pr.goal_trend_annotate(measure_name,**self.goal_dicts)
            a=pr.goal_acheivement_loss_annotate(measure_name, **self.goal_dicts)
            a=pr.goalconsecutive_annotate(measure_name,**self.goal_dicts)
            a=pr.goal_monotonicity_annotate(measure_name,**self.goal_dicts) 
            a=pr.peer_gap_annotate(measure_name,**self.measure_dicts)
            a=pr.peer_trend_annotate(measure_name,**self.measure_dicts)
            a=pr.peer_acheivement_loss_annotate(measure_name, **self.measure_dicts) 
            a=pr.peerconsecutive_annotate(measure_name,**self.measure_dicts)
            a=pr.peer_monotonicity_annotate(measure_name,**self.measure_dicts)
        
        return self.input_graph
