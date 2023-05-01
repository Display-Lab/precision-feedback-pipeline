



import pandas as pd
from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector
#from insert_annotate import insert_annotate

from bit_stomach.prepare_data_annotate import Prepare_data_annotate

class Bit_stomach:
    def __init__(self,input_graph:Graph,performance_data:pd.DataFrame):
        self.measure_dicts={}
        self.goal_dicts={}
        self.goal_comparison_dicts={}
        self.top_10_dicts={}
        self.top_25_dicts={}
        self.performance_data_df=performance_data
        self.input_graph=input_graph
        s=URIRef("http://example.com/app#display-lab")
        p=URIRef('http://example.com/slowmo#IsAboutMeasure')
        p1=URIRef("http://example.com/slowmo#WithComparator")
        p3=URIRef('http://schema.org/name')
        o5=URIRef("http://purl.obolibrary.org/obo/PSDO_0000126")
        o55=URIRef("http://purl.obolibrary.org/obo/PSDO_0000128")
        o555=URIRef("http://purl.obolibrary.org/obo/PSDO_0000129")
        p5=RDF.type
        p6=URIRef("http://example.com/slowmo#ComparisonValue")
        p21=URIRef("http://purl.org/dc/terms/title")
        p22=URIRef("http://schema.org/name")
        o21=Literal("PEERS")
        o22=Literal("peers") 
        o212=Literal("TOP_10")
        o222=Literal("top_10") 
        o2122=Literal("TOP_25")
        o2222=Literal("top_25")
        self.input_graph=input_graph
        def remove_annotate(self):
            s12 = URIRef('http://example.com/app#display-lab')
            p12=URIRef('http://example.com/slowmo#IsAboutPerformer')
            o12=BNode('p1')
            self.input_graph.remove((o12,None,None))

        def insert_blank_nodes_top_25(self):
        #insert blank nodes for social comparators for each measure
            for sw,pw,ow in self.input_graph.triples((s, p, None)):
                s1=ow
                o11=BNode()
                self.input_graph.add((s1,p1,o11))  
                s11=o11
                self.input_graph.add((s11,p5,o55))
                self.input_graph.add((s11,p21,o2122))
                self.input_graph.add((s11,p22,o2222))
        def insert_blank_nodes_top_10(self):
        #insert blank nodes for social comparators for each measure
            for sw,pw,ow in self.input_graph.triples((s, p, None)):
                s1=ow
                o11=BNode()
                self.input_graph.add((s1,p1,o11))  
                s11=o11
                self.input_graph.add((s11,p5,o555))
                self.input_graph.add((s11,p21,o212))
                self.input_graph.add((s11,p22,o222))    
            
        def insert_blank_nodes_peers(self):
        #insert blank nodes for social comparators for each measure
            for sw,pw,ow in self.input_graph.triples((s, p, None)):
                s1=ow
                o11=BNode()
                self.input_graph.add((s1,p1,o11))  
                s11=o11
                self.input_graph.add((s11,p5,o5))
                self.input_graph.add((s11,p21,o21))
                self.input_graph.add((s11,p22,o22))
        #get comparison values for goal from base graph and get Blank nodes for both goal and peer comparators
        def check_rerunkey(self):
            rerunkey=0
            for sq,pq,oq in self.input_graph.triples((s, p, None)):
                s1=oq
                for s2,p2,o2 in self.input_graph.triples((s1,p1,None)):
                    
                    s3=o2
                    for s4,p4,o4 in self.input_graph.triples((s3,p3,None)):
                        if str(o4)=="peers":
                            rerunkey=1
            return rerunkey
        # self.rerunkey= check_rerunkey(self)
        # if(self.rerunkey==0):
        insert_blank_nodes_top_10(self)
        insert_blank_nodes_top_25(self)
        insert_blank_nodes_peers(self)
        # if(self.rerunkey==1):
        #     remove_annotate(self)
           
        for s,p,o in self.input_graph.triples((s, p, None)):
            s1=o
            for s2,p2,o2 in self.input_graph.triples((s1,p1,None)):
                self.measure_dicts[s1]=o2
                s3=o2
                for s4,p4,o4 in self.input_graph.triples((s3,p3,None)):
                    if str(o4)=="top_10":
                        #print(o2)
                        self.top_10_dicts[s1]=o2
                    if str(o4)=="top_25":
                        #print(o2)
                        self.top_25_dicts[s1]=o2

                    if str(o4)=="goal":
                        #print(o2)
                        self.goal_dicts[s1]=o2
                        for s8,p8,o8 in self.input_graph.triples((s3,p6,None)):
                            self.goal_comparison_dicts[s1]=o8
        

    def annotate(self):
        a=self.input_graph
        goaldf=pd.DataFrame(self.goal_comparison_dicts.items())
        
#socialdf=pd.DataFrame(social_comparison_dicts.items())
        goaldf1=pd.DataFrame(self.goal_comparison_dicts.items())
        goaldf1.columns =['measure', 'goal_comparison_value']
        
        pr=Prepare_data_annotate(a,self.performance_data_df,goaldf1)

        measure_list=[]
        self.performance_data_df["measure"]=self.performance_data_df["measure"].str.decode(encoding="UTF-8")

        measure_list=self.performance_data_df["measure"].drop_duplicates()
        
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
            a=pr.top_10_gap_annotate(measure_name,**self.top_10_dicts)
            a=pr.top_10_trend_annotate(measure_name,**self.top_10_dicts)
            a=pr.top_10_acheivement_loss_annotate(measure_name,**self.top_10_dicts)
            a=pr.top_10consecutive_annotate(measure_name,**self.top_10_dicts)
            a=pr.top_10_monotonicity_annotate(measure_name,**self.top_10_dicts)
            a=pr.top_25_gap_annotate(measure_name,**self.top_25_dicts)
            a=pr.top_25_trend_annotate(measure_name,**self.top_25_dicts)
            a=pr.top_25_acheivement_loss_annotate(measure_name,**self.top_25_dicts)
            a=pr.top_25consecutive_annotate(measure_name,**self.top_25_dicts)
            a=pr.top_25_monotonicity_annotate(measure_name,**self.top_25_dicts)
        return self.input_graph
