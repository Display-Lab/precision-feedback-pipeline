import json
import sys
import warnings
import time
import logging
import json
import random
#from asyncore import read

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef, BNode
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

        
        self.message_code=message_code
    def apply_preferences(self):
        Message_Format={}
        Display_Format={}
        for (k, v) in self.preferences.items():
            for (k1,v1) in v.items():
                for (k2,v2) in v1.items():
                    
                    if(k1=="Message_Format"):
                        k2=int(k2)
                        Message_Format[k2]=v2
                    if(k1=="Display_Format"):
                        Display_Format[k2]=v2
        # for k,v in Message_Format.items():
            
        #     print(type(k))
        #     print(k,v)
        # for k,v in Display_Format.items():
        #     print(k,v)
        p4=URIRef("psdo:PerformanceSummaryTextualEntity")
        for x in range(len(self.y)):
            s=self.y[x]
            for s3,p3,o3 in self.spek_tp.triples((s,self.p2,None)):
                score=int(o3)
                

            for s1,p32,o1 in self.spek_tp.triples((s,p4,None)):
                o2=float(o1)
                for k,v in Message_Format.items():
                    if k==o2:
                        value=float(v)
                        score1=score*value
                        score1=Literal(score1)
                        self.spek_tp.remove((s,self.p2,o3))
                        self.spek_tp.add((s,self.p2,score1))
                # print(type(o2))
        #         text=o1
        p5=URIRef("psdo:PerformanceSummaryDisplay")
        for x in range(len(self.y)):
            s=self.y[x]
            for s3,p3,o3 in self.spek_tp.triples((s,self.p2,None)):
                score=float(o3)
            for s1,p32,o1 in self.spek_tp.triples((s,p5,None)): 
                o1=str(o1)
                for k,v in Display_Format.items():
                    if o1==k:
                        value=float(v)  
                        score1=score*value
                        score1=Literal(score1)
                        self.spek_tp.remove((s,self.p2,o3))
                        self.spek_tp.add((s,self.p2,score1))

                
        #indv_preferences_df = pd.json_normalize(self.preferences)
        # display_preferences_df =indv_preferences_df [['Utilities.Display_Format.short_sentence_with_no_chart', 'Utilities.Display_Format.bar_chart','Utilities.Display_Format.line_graph']]
        # message_preferences_df =indv_preferences_df[['Utilities.Message_Format.1','Utilities.Message_Format.2','Utilities.Message_Format.16','Utilities.Message_Format.24','Utilities.Message_Format.18','Utilities.Message_Format.11','Utilities.Message_Format.22','Utilities.Message_Format.14','Utilities.Message_Format.21']]
        #indv_preferences_df.to_csv("indv_pref.csv")
        # message_preferences_df.to_csv("mesaa.csv")
    def apply_history(self):
        # for x in range(len(self.scores)):
        #         print(self.scores[x])
        Text=[]
        Display=[]
        Measure_Name=[]
        nodes1=[]
        for (k, v) in self.history.items():
            # print(k,v)
            for (k1,v1) in v.items():
                
                if(k1=="Text"):
                    # print(k1)
                    # print(v1)
                    Text.append(v1)
                if(k1=="Measure Name"):
                    Measure_Name.append(v1)
                if(k1=="Display"):
                    Display.append(v1)
    
        s_m1=self.get_selected_message()
        texta= s_m1["text"]
        texta=str(texta)
        if texta == "No message selected":
            return self.node
        displaya=s_m1["display"]
        displaya=str(displaya)
        measure_namea=s_m1["Measure Name"]
        measure_namea=str(measure_namea)
        if displaya in Display or measure_namea in Measure_Name or texta or Text:
            self.score_max=float(self.score_max)
            self.scores.remove(self.score_max)
            if len(self.scores)!=0:
                self.score_max=max(self.scores)
            self.score_max = Literal(self.score_max)
        # print(self.score_max)
            for s4,p4,o4 in self.spek_tp.triples((None,self.p2,self.score_max)):
                self.node=s4
            # print(self.node)
            return self.node
        else:
            return self.node
     

                
            
            

    def select(self):
        self.scores=[]
        nodes=[]
        if len(self.y)!=0:
            for x in range(len(self.y)):
                s=self.y[x]
                for s3,p3,o3 in self.spek_tp.triples((s,self.p2,None)):
                    score=float(o3)
                    self.scores.append(score)
            if len(self.scores)!=0:
                self.score_max=max(self.scores)
            self.score_max = Literal(self.score_max)
            #print(score_max)
            for s4,p4,o4 in self.spek_tp.triples((None,self.p2,self.score_max)):
                node=s4
                nodes.append(node)
            
            # print(self.score_max)

            self.node=random.choice(nodes)
            #self.apply_history(self)
            
            
            
        else:
            self.node="No message selected"

        # if len(self.y)!=0:
        #     self.node=random.choice(self.y)
        # else:
        #     self.node="No message selected"
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
            p=URIRef("psdo:PerformanceSummaryDisplay")
            p2=URIRef("name")
            p3=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
            p4=URIRef("psdo:PerformanceSummaryTextualEntity")
            p5=URIRef("http://example.com/slowmo#RegardingMeasure")
            p7=URIRef("http://example.com/slowmo#RegardingComparator")
            p11=URIRef("http://purl.org/dc/terms/title")
            p121=URIRef("http://purl.org/dc/terms/title")
            # s_m["node"]=self.node
            for s1,p32,o1 in self.spek_tp.triples((s,p4,None)):
                #print(o1)
                text=o1
                f="http://schema.org/"+text
                p23=URIRef(f)
                for s24,p24,o24 in self.message_code.triples((None,p23,None)):
                    s_m["text"]=o24
                    # print(o24)
            
            for s1,p1,o1 in self.spek_tp.triples((s,p,None)):
                #print(o1)
                s_m["display"]=o1
            for s4,p4,o4 in self.spek_tp.triples((s,p3,None)):
                s5=o4
                for s6,p6,o6 in self.spek_tp.triples((s5,p5,None)):
                    s_m["Measure Name"]=o6
                    s11=o6
                    #print(o6)
                    
                    #     s_m["Title"]=o12
                for s8,p8,o8 in self.spek_tp.triples((s5,p7,None)):
                    s10=o8
                    for  s9,p9,o9 in self.spek_tp.triples((s10,p11,None)):
                        s_m["Comparator Type"]=o9

            s11= BNode(s_m["Measure Name"]  )
            # print(s11)     
            for  s02,p02,o02 in self.spek_tp.triples((s11,p11,None)):
                s_m["Title"]=o02    

            
            # for k,v in s_m.items():
            #     print(k,v)    
            
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
