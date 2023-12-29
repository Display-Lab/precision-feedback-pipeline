from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF
from loguru import logger
import pandas as pd
import sys

## Logging setup
logger.remove()
logger.add(sys.stdout, colorize=True, format="{level} | {message}")
from bit_stomach.prepare_data_annotate import Prepare_data_annotate
from bit_stomach.student_t_cleaner import student_t_cleaner

class Bit_stomach:
    def __init__(self,performer_graph:Graph,performance_data:pd.DataFrame):
        self.peer_dicts={} #This contains blank nodes as keys and peer comparator title
        self.top_10_dicts={}#This contains blank nodes as keys and top 10 comparator title
        self.top_25_dicts={}#This contains blank nodes as keys and top 25 comparator title
        self.goal_dicts={}#This contains blank nodes as keys and goal comparator title
       
        #cleaned dataframe as self.performance_data_df:
        try:
            self.performance_data_df=student_t_cleaner(performance_data)
        except ValueError as e:
            raise e
            
        
        self.performer_graph=performer_graph
        
        

        

        def insert_blank_nodes_top_25(self):
        #insert blank nodes for top 25 comparator for each measure
            for sw,pw,ow in self.performer_graph.triples((URIRef("http://example.com/app#display-lab"), URIRef('http://example.com/slowmo#IsAboutMeasure'), None)):
                s1=ow
                o11=BNode()
                self.performer_graph.add((s1,URIRef("http://example.com/slowmo#WithComparator"),o11))  
                s11=o11
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000095")))
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000128")))
                self.performer_graph.add((s11,URIRef("http://purl.org/dc/terms/title"),Literal("TOP_25")))
                self.performer_graph.add((s11,URIRef("http://schema.org/name"),Literal("top_25")))
        def insert_blank_nodes_top_10(self):
        #insert blank nodes for top 10 comparator for each measure
            for sw,pw,ow in self.performer_graph.triples((URIRef("http://example.com/app#display-lab"), URIRef('http://example.com/slowmo#IsAboutMeasure'), None)):
                s1=ow
                o11=BNode()
                self.performer_graph.add((s1,URIRef("http://example.com/slowmo#WithComparator"),o11))  
                s11=o11
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000095")))
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000129")))
                self.performer_graph.add((s11,URIRef("http://purl.org/dc/terms/title"),Literal("TOP_10")))
                self.performer_graph.add((s11,URIRef("http://schema.org/name"),Literal("top_10")))    
            
        def insert_blank_nodes_peers(self):
        #insert blank nodes for peers comparator for each measure
            for sw,pw,ow in self.performer_graph.triples((URIRef("http://example.com/app#display-lab"), URIRef('http://example.com/slowmo#IsAboutMeasure'), None)):
                s1=ow
                o11=BNode()
                self.performer_graph.add((s1,URIRef("http://example.com/slowmo#WithComparator"),o11))  
                s11=o11
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000095")))
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000126")))
                self.performer_graph.add((s11,URIRef("http://purl.org/dc/terms/title"),Literal("PEERS")))
                self.performer_graph.add((s11,URIRef("http://schema.org/name"),Literal("peers")))
        
        def insert_blank_nodes_goal(self):
        #insert blank nodes for goal comparator for each measure
            for sw,pw,ow in self.performer_graph.triples((URIRef("http://example.com/app#display-lab"), URIRef('http://example.com/slowmo#IsAboutMeasure'), None)):
                s1=ow
                o11=BNode()
                self.performer_graph.add((s1,URIRef("http://example.com/slowmo#WithComparator"),o11))  
                s11=o11
                self.performer_graph.add((s11,RDF.type,URIRef("http://purl.obolibrary.org/obo/PSDO_0000094")))
                self.performer_graph.add((s11,URIRef("http://purl.org/dc/terms/title"),Literal("GOAL")))
                self.performer_graph.add((s11,URIRef("http://schema.org/name"),Literal("goal")))
        
        
        
        
        insert_blank_nodes_top_10(self)
        insert_blank_nodes_top_25(self)
        insert_blank_nodes_peers(self)
        insert_blank_nodes_goal(self)
        
        #extract blank nodes for each comparator   
        for s,p,o in self.performer_graph.triples((URIRef("http://example.com/app#display-lab"), URIRef('http://example.com/slowmo#IsAboutMeasure'), None)):
            s1=o
            for s2,p2,o2 in self.performer_graph.triples((s1,URIRef("http://example.com/slowmo#WithComparator"),None)):
                
                s3=o2
                for s4,p4,o4 in self.performer_graph.triples((s3,URIRef('http://schema.org/name'),None)):
                    if str(o4)=="top_10":
                        #print(o2)
                        self.top_10_dicts[s1]=o2
                    if str(o4)=="top_25":
                        #print(o2)
                        self.top_25_dicts[s1]=o2
                    if str(o4)=="goal":
                        #print(o2)
                        self.goal_dicts[s1]=o2
                    if str(o4)=="peers":
                        #print(o2)
                        self.peer_dicts[s1]=o2

                   
                        
        

    def annotate(self):
        #prepare data before annotating
        prepared_data=Prepare_data_annotate(self.performer_graph,self.performance_data_df)
        measure_list=[]
        self.performance_data_df["measure"]=self.performance_data_df["measure"].str.decode(encoding="UTF-8")
        measure_list=self.performance_data_df["measure"].drop_duplicates()
        
        for index, element in enumerate(measure_list):
            measure_name=element

            self.performer_graph=prepared_data.goal_gap_annotate(measure_name,**self.goal_dicts)
            self.performer_graph=prepared_data.goal_trend_annotate(measure_name,**self.goal_dicts)
            self.performer_graph=prepared_data.goal_acheivement_loss_annotate(measure_name, **self.goal_dicts)
            self.performer_graph=prepared_data.goalconsecutive_annotate(measure_name,**self.goal_dicts)
            self.performer_graph=prepared_data.goal_monotonicity_annotate(measure_name,**self.goal_dicts) 
            self.performer_graph=prepared_data.peer_gap_annotate(measure_name,**self.peer_dicts)
            self.performer_graph=prepared_data.peer_trend_annotate(measure_name,**self.peer_dicts)
            self.performer_graph=prepared_data.peer_acheivement_loss_annotate(measure_name, **self.peer_dicts) 
            self.performer_graph=prepared_data.peerconsecutive_annotate(measure_name,**self.peer_dicts)
            self.performer_graph=prepared_data.peer_monotonicity_annotate(measure_name,**self.peer_dicts)
            self.performer_graph=prepared_data.top_10_gap_annotate(measure_name,**self.top_10_dicts)
            self.performer_graph=prepared_data.top_10_trend_annotate(measure_name,**self.top_10_dicts)
            self.performer_graph=prepared_data.top_10_acheivement_loss_annotate(measure_name,**self.top_10_dicts)
            self.performer_graph=prepared_data.top_10consecutive_annotate(measure_name,**self.top_10_dicts)
            self.performer_graph=prepared_data.top_10_monotonicity_annotate(measure_name,**self.top_10_dicts)
            self.performer_graph=prepared_data.top_25_gap_annotate(measure_name,**self.top_25_dicts)
            self.performer_graph=prepared_data.top_25_trend_annotate(measure_name,**self.top_25_dicts)
            self.performer_graph=prepared_data.top_25_acheivement_loss_annotate(measure_name,**self.top_25_dicts)
            self.performer_graph=prepared_data.top_25consecutive_annotate(measure_name,**self.top_25_dicts)
            self.performer_graph=prepared_data.top_25_monotonicity_annotate(measure_name,**self.top_25_dicts)
        return self.performer_graph
