import warnings
import time
import logging
import random
#from asyncore import read

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF



# from .load_for_real import load
# from load import read, transform,read_contenders,read_measures,read_comparators
# from score import score, select,apply_indv_preferences,apply_history_message

# load()

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
# Read graph and convert to dataframe
start_time = time.time()
class Esteemer():
    def __init__(self, spek_tp, preferences , history):
        self.y=[]
        self.spek_tp=spek_tp
        self.preferences=preferences
        self.history=history
        self.s=URIRef("http://example.com/app#display-lab")
        self.p=URIRef("http://example.com/slowmo#HasCandidate")
        self.p1=URIRef("slowmo:acceptable_by")
        self.p2=URIRef('http://example.com/slowmo#Score')
        self.o2=Literal(1)
        
        for s,p,o in self.spek_tp.triples( (self.s, self.p, None) ):
            s1= o
            for s,p,o in self.spek_tp.triples((s1,self.p1,None)):
                self.spek_tp.add((s,self.p2,self.o2))
                self.y.append(s)
                # print(s)
        
    def select(self):
        self.scores=[]
        nodes=[]
        if len(self.y)!=0:
            self.node=random.choice(self.y)
        else:
            self.node="No message selected"

        if self.node== "No message selected":
            return self.node,self.spek_tp
        else:
            o2=URIRef("http://example.com/slowmo#selected")
            self.spek_tp.add((self.node,RDF.type,o2))
            return self.node,self.spek_tp

    def get_selected_message(self):
        s_m={}
        if self.node== "No message selected":
            s_m["text"]="No message selected"
            return s_m 
        else:
            s=self.node
            p1=URIRef("psdo:PerformanceSummaryTextualEntity")
            pwed=URIRef("slowmo:acceptable_by")
            p3=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
            p4=URIRef("http://example.com/slowmo#RegardingMeasure")
            p8=URIRef("http://example.com/slowmo#name")
            p10= URIRef("http://purl.org/dc/terms/title")
            p12=URIRef("http://purl.obolibrary.org/obo/IAO_0000573")
            p13=URIRef("http://purl.obolibrary.org/obo/STATO_0000166")
            p20=URIRef("http://example.com/slowmo#AncestorTemplate")
            pqd=URIRef("http://example.com/slowmo#PerformanceGapSize")
            pqw=URIRef("http://example.com/slowmo#PerformanceTrendSlope")
            p232= URIRef("psdo:PerformanceSummaryDisplay")
            Display=["Text-only", "bar chart", "line graph"]
            sw=0
            o2wea=[]
            
            
            for s21,p21,o21 in self.spek_tp.triples((s,p20,None)):
                s_m["Template ID"] = o21
            for s2,p2,o2 in self.spek_tp.triples((s,p1,None)):
                s_m["text"] = o2
            # for s212,p212,o212 in self.spek_tp.triples((s,p232,None)):
               
            s_m["Display"]=random.choice(Display)
            for s9,p9,o9 in self.spek_tp.triples((s,p8,None)):
                s_m["Comparator Type"] = o9
            for s2we,p2we,o2we in self.spek_tp.triples((s,pwed,None)):
                o2wea.append(o2we)
            # print(*o2wea)
            s_m["Acceptable By"] = o2wea

            
            
            

            
                
            

            for s5,p5,o5 in self.spek_tp.triples((s,p3,None)):
                s6=o5
                # print(o5)
                for s7,p7,o7 in self.spek_tp.triples((s6,p4,None)):
                    s_m["Measure Name"]=o7
                    s10= BNode(o7)
                    for s11,p11,o11 in self.spek_tp.triples((s10,p10,None)):
                        s_m["Title"]=o11
                for s14,p14,o14 in self.spek_tp.triples((s6,RDF.type,None)):
                    #print(o14)
                    if o14==p12:
                        s_m["Display"]="line graph"
                        sw=1
                    if o14==p13:
                        s_m["Display"]="bar chart"
                        if sw==1:
                            s_m["Display"]= "line graph,bar chart"
                

            
                  

            
            return s_m
    
# logging.critical("--score and select %s seconds ---" % (time.time() - start_time1))
# print(finalData)

# time_taken = time.time()-start_time
logging.critical("---total esteemer run time according python script %s seconds ---" % (time.time() - start_time))

"""with open('data.json', 'a') as f:
    f.write(finalData + '\n')"""
