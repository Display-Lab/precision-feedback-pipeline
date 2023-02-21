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


warnings.filterwarnings("ignore", category=FutureWarning)
class CandidateSmasher:
    def __init__(self,spek_bs:Graph,templates:Graph):
        self.a=spek_bs
        self.b=templates
        self.measure_dicts={}
        self.social_dicts={}
        self.goal_dicts={}
        self.social_comparison_dicts={}
        self.goal_comparison_dicts={}
        self.annotate_dicts={}
        self.graph_type_list=[]



        self.so=URIRef("http://example.com/app#display-lab")
        self.sq12=URIRef("http://example.com/app#display-lab")
        self.pq12=URIRef("http://example.com/slowmo#HasCandidate")
        self.po=URIRef('http://example.com/slowmo#IsAboutMeasure')
        self.p1=URIRef("http://example.com/slowmo#WithComparator")
        self.p3=URIRef('http://schema.org/name')
        self.o5=URIRef("http://purl.obolibrary.org/obo/psdo_0000095")
        self.p5=RDF.type
        self.p6=URIRef("http://example.com/slowmo#ComparisonValue")
        self.p21=URIRef("http://purl.org/dc/terms/title")
        self.p22=URIRef("http://schema.org/name")
        self.o21=Literal("PEERS")
        self.o22=Literal("peers") 
        self.p23=URIRef("http://schema.org/@templates")
        self.p24=URIRef("http://purl.obolibrary.org/obo/IAO_0000136")
        self.p25=RDF.type
        self.pq13=URIRef("psdo:PerformanceSummaryDisplay")
        self.pq14=URIRef("psdo:PerformanceSummaryTextualEntity")
        self.pq15=URIRef("http://schema.org/name")

        self.cp=RDF.type
        self.co=URIRef("http://purl.obolibrary.org/obo/cpo_0000053")
        self.cp1=URIRef("http://example.com/slowmo#name")
        self.cp2=URIRef("psdo:PerformanceSummaryTextualEntity")
        self.cp3=URIRef("psdo:PerformanceSummaryDisplay")
        self.cp4=RDF.type
        self.cop4=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
        self.cp23=URIRef("http://example.com/slowmo#RegardingComparator")
        self.cp24=URIRef("http://example.com/slowmo#RegardingMeasure")
        self.cp25="http://purl.obolibrary.org/obo/psdo_0000102"
        self.cp26=URIRef("http://example.com/slowmo#AncestorPerformer")
        self.cp27=URIRef("http://example.com/slowmo#AncestorTemplate")
        self.cp28=URIRef("http://example.com/slowmo#Candidate")


        self.cp21=URIRef("http://example.com/slowmo#AncestorTemplate")
# f1 = open("test23.txt", "w")
# f2 = open("test24.txt", "w")
        self.ac=[]
        self.ab=[]
        self.text_dicts={}
        self.name_dicts={}
        self.display_dicts={}
        self.template_type_dicts={}
        self.candidate_id_dicts={}
        self.goal_dicts={}
        self.top_10_dicts={}
        self.top_25_dicts={}
        self.graph_type_list=[]
        self.graph_type_list1=[]

    def get_graph_type(self):
        for s,p,o in self.a.triples((self.so, self.po, None)):
            s1=o
            goal_nodes=[]
            for s2,p2,o2 in self.a.triples((s1,self.p1,None)):
                
                self.measure_dicts[s1]=o2
                s3=o2
                final_node_type=[]
                node_type=[]
                node_type1=[]
                node_type2=[]
                node_type.append(s1)
                node_type.append(o2)
                for s4,p4,o4 in self.a.triples((s3,self.p3,None)):
                        #print(o4)
                        if str(o4)=="goal":
                            self.goal_dicts[s1]=o2
                        if str(o4)=="top_10":
                            self.top_10_dicts[s1]=o2
                        if str(o4)=="top_25":
                            self.top_25_dicts[s1]=o2
                        
                
                # self.a.remove((s1,self.p1,o2))
                # for s2,p2,o21 in self.a.triples((s1,self.p1,None)):
                #     #self.goal_dicts[s1]=o2
                #     self.a.remove((s1,self.p1,o21))
                #     for s2,p2,o212 in self.a.triples((s1,self.p1,None)):
                #         print(o212)
                # self.a.add((s1,self.p1,o2))
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if str(o82) != self.cp25:
                        # print(o82)
                        node_type.append(str(o82))
        
                    
            node_type_tuple=tuple(node_type)
        
            self.graph_type_list.append(node_type_tuple)
       
        
        new = pd.DataFrame.from_dict(self.goal_dicts, orient ='index')
        new= new.reset_index()
        new = new.rename({"index":"Measure_Name"}, axis=1)
        new = new.rename({0:"Comparator_Node"}, axis=1)
        self.goal_types=[]
        for rowIndex, row in new.iterrows(): 
            s1=row["Measure_Name"]
            o2=row["Comparator_Node"]
            node_type1=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type1:
                        node_type1.append(s1)
                    if o2 not in node_type1:
                        node_type1.append(o2)
                    if str(o82) != self.cp25:
                        node_type1.append(str(o82))
            node_type_tuple1=tuple(node_type1)
            node_type_tuple1=node_type_tuple1
            self.goal_types.append(node_type_tuple1)

        new1 = pd.DataFrame.from_dict(self.top_10_dicts, orient ='index')
        new1= new1.reset_index()
        new1 = new1.rename({"index":"Measure_Name"}, axis=1)
        new1 = new1.rename({0:"Comparator_Node"}, axis=1)
        self.top_10_types=[]
        for rowIndex, row in new1.iterrows(): 
            s1=row["Measure_Name"]
            o2=row["Comparator_Node"]
            node_type2=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type2:
                        node_type2.append(s1)
                    if o2 not in node_type2:
                        node_type2.append(o2)
                    if str(o82) != self.cp25:
                        node_type2.append(str(o82))
            node_type_tuple2=tuple(node_type2)
            node_type_tuple2=node_type_tuple2
            self.top_10_types.append(node_type_tuple2)
        
        new2 = pd.DataFrame.from_dict(self.top_25_dicts, orient ='index')
        new2= new2.reset_index()
        new2 = new2.rename({"index":"Measure_Name"}, axis=1)
        new2 = new2.rename({0:"Comparator_Node"}, axis=1)
        # new2.to_csv("top_25.csv")
        self.top_25_types=[]
        for rowIndex, row in new2.iterrows(): 
            s1=row["Measure_Name"]
            o2=row["Comparator_Node"]
            node_type3=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type3:
                        node_type3.append(s1)
                    if o2 not in node_type3:
                        node_type3.append(o2)
                    if str(o82) != self.cp25:
                        node_type3.append(str(o82))
            node_type_tuple3=tuple(node_type3)
            node_type_tuple3=node_type_tuple3
            self.top_25_types.append(node_type_tuple3)
        
        self.df_graph = pd.DataFrame(self.graph_type_list)
        self.goal_types=pd.DataFrame(self.goal_types)
        self.top_10_types=pd.DataFrame(self.top_10_types)
        self.top_25_types=pd.DataFrame(self.top_25_types)
        self.df_graph = self.df_graph.rename({0:"Measure_Name"}, axis=1)
        self.df_graph = self.df_graph.rename({1:"Comparator_Node"}, axis=1)
        self.df_graph = self.df_graph.rename({2:"graph_type1"}, axis=1)
        self.df_graph = self.df_graph.rename({3:"graph_type2"}, axis=1)
        self.df_graph = self.df_graph.rename({4:"graph_type3"}, axis=1)
        self.df_graph = self.df_graph.rename({5:"graph_type4"}, axis=1)
        self.df_graph = self.df_graph.rename({6:"graph_type5"}, axis=1)
        self.df_graph = self.df_graph.rename({7:"graph_type6"}, axis=1)
        self.df_graph = self.df_graph.fillna(0)
        self.df_graph["comparator_type"]="peers"
        self.df_graph=self.df_graph.reset_index(drop=True)
        # self.df_graph.to_csv("graph_df.csv")
        # self.df_graph1=pd.DataFrame(self.graph_type_list1)
        self.goal_types = self.goal_types.rename({0:"Measure_Name"}, axis=1)
        self.goal_types = self.goal_types.rename({1:"Comparator_Node"}, axis=1)
        self.goal_types = self.goal_types.rename({2:"graph_type1"}, axis=1)
        self.goal_types = self.goal_types.rename({3:"graph_type2"}, axis=1)
        self.goal_types = self.goal_types.rename({4:"graph_type3"}, axis=1)
        self.goal_types = self.goal_types.rename({5:"graph_type4"}, axis=1)
        self.goal_types = self.goal_types.rename({6:"graph_type5"}, axis=1)
        self.goal_types = self.goal_types.rename({7:"graph_type6"}, axis=1)
        self.goal_types = self.goal_types.fillna(0)
        self.goal_types["comparator_type"]="goal"
        self.goal_types=self.goal_types.reset_index(drop=True)
        # self.goal_types.to_csv("goal_types.csv")


        self.top_10_types = self.top_10_types.rename({0:"Measure_Name"}, axis=1)
        self.top_10_types = self.top_10_types.rename({1:"Comparator_Node"}, axis=1)
        self.top_10_types = self.top_10_types.rename({2:"graph_type1"}, axis=1)
        self.top_10_types = self.top_10_types.rename({3:"graph_type2"}, axis=1)
        self.top_10_types = self.top_10_types.rename({4:"graph_type3"}, axis=1)
        self.top_10_types = self.top_10_types.rename({5:"graph_type4"}, axis=1)
        self.top_10_types = self.top_10_types.rename({6:"graph_type5"}, axis=1)
        self.top_10_types = self.top_10_types.rename({7:"graph_type6"}, axis=1)
        self.top_10_types = self.top_10_types.fillna(0)
        # self.top_10=self.top_10_types
        self.top_10_types["comparator_type"]="top_10"
        self.top_10_types=self.top_10_types.reset_index(drop=True)
        # self.top_10_types.to_csv("top_10_types.csv")
        # self.top_10.to_csv("top_10.csv")

        self.top_25_types = self.top_25_types.rename({0:"Measure_Name"}, axis=1)
        self.top_25_types = self.top_25_types.rename({1:"Comparator_Node"}, axis=1)
        self.top_25_types = self.top_25_types.rename({2:"graph_type1"}, axis=1)
        self.top_25_types = self.top_25_types.rename({3:"graph_type2"}, axis=1)
        self.top_25_types = self.top_25_types.rename({4:"graph_type3"}, axis=1)
        self.top_25_types = self.top_25_types.rename({5:"graph_type4"}, axis=1)
        self.top_25_types = self.top_25_types.rename({6:"graph_type5"}, axis=1)
        self.top_25_types = self.top_25_types.rename({7:"graph_type6"}, axis=1)
        self.top_25_types = self.top_25_types.fillna(0)
        # self.top_25=self.top_25_types
        self.top_25_types["comparator_type"]="top_25"
        self.top_25_types=self.top_25_types.reset_index(drop=True)
        # self.top_25_types.to_csv("top_25_types.csv")
        df1 = self.top_10_types.drop(self.top_10_types.columns[-1],axis=1)
        df1=df1.drop(['Comparator_Node'], axis=1)
        df1=df1.loc[df1['graph_type1'] != 0]
        df1=df1.reset_index(drop="True")
        Measure_list_top_25=[]
        top_10_list = list(df1.itertuples(index=False, name=None))
        for x in range(len(top_10_list)):
            print(top_10_list[x])
        df2 = self.top_25_types.drop(self.top_25_types.columns[-1],axis=1)
        df2=df2.drop(['Comparator_Node'], axis=1)
        df2=df2.loc[df2['graph_type1'] != 0]
        df2=df2.reset_index(drop="True")
        top_25_list=list(df2.itertuples(index=False, name=None))
        for x in range(len(top_25_list)):
            if(top_25_list[x] in top_10_list):
                Measure_list_top_25.append(top_25_list[x][0])

        # df2 = self.top_25_types.drop(self.top_25_types.columns[-1],axis=1)
        
        # df2=df2.loc[df2['graph_type1'] != 0]
        # df2=df2.reset_index(drop="True")
       
        # top_25_list = df2.Measure_Name.values.tolist()
        # self.df_graph = self.df_graph[self.df_graph.Measure_Name.isin(top_25_list) == False]
       
       

        
        self.top_25_types = self.top_25_types[self.top_25_types.Measure_Name.isin(Measure_list_top_25) == False]
        # self.df_graph = self.df_graph[self.df_graph.Measure_Name.isin(top_10_list) == False]
       
        # for x in range(len(top_25_list)):
        #     print(top_25_list[x])
        #self.df_graph = self.df_graph[self.df_graph.Measure_Name.isin(top_10_list) == False]
        self.df_merged = pd.concat([self.df_graph, self.goal_types,self.top_10_types,self.top_25_types], ignore_index=True, sort=False)
        self.df_merged =self.df_merged.fillna(0)
        # self.df_merged.to_csv("df_merged.csv")
        return self.df_merged

     

    def get_template_data(self):
        for s,p,o in self.b.triples((None,self.p23,None)):
            self.ac.append(str(o))
        a25_dicts={}
        a26_dicts={}
        a27_dicts={}
        templatetype_dicts={}
        for x in range(len(self.ac)):
            s24=URIRef(self.ac[x])
            af=[]
            ab=[]
            for s29,p29,o29 in self.b.triples((s24,self.pq13,None)):
                a25_dicts[self.ac[x]]=str(o29)
            for s30,p30,o30 in self.b.triples((s24,self.pq14,None)):
                a26_dicts[self.ac[x]]=str(o30)
            for s31,p31,o31 in self.b.triples((s24,self.pq15,None)):
                a27_dicts[self.ac[x]]=str(o31)

            for s,p,o in self.b.triples((s24,self.p24,None)):
                s25=o
                for s,p,o in self.b.triples((s25,self.p25,None)):
                    templatetype=str(o)
                    ab.append(templatetype)
            ad=tuple(ab)
            templatetype_dicts[self.ac[x]]=ad
        display_dicts=a25_dicts
        text_dicts=a26_dicts
        name_dicts=a27_dicts
        template_type_dicts=templatetype_dicts
        self.df_text = pd.DataFrame.from_dict(text_dicts,orient='index')
        self.df_text = self.df_text.rename({0:"text"}, axis=1)
        self.df_display_dicts=pd.DataFrame.from_dict(display_dicts,orient='index')
        self.df_display_dicts = self.df_display_dicts.rename({0:"display"}, axis=1)
        self.df_name_dicts=pd.DataFrame.from_dict(name_dicts,orient='index')
        self.df_name_dicts = self.df_name_dicts.rename({0:"name"}, axis=1)
        self.df_template_type_dicts=pd.DataFrame.from_dict(template_type_dicts,orient='index')
        self.df_template_type_dicts = self.df_template_type_dicts.rename({0:"template_type_dicts"}, axis=1)
        self.df=pd.concat([self.df_text, self.df_display_dicts,self.df_name_dicts,self.df_template_type_dicts], axis=1)
       
        self.df = self.df.rename({1:"template_type_dicts1"}, axis=1)
        self.df = self.df.rename({2:"template_type_dicts2"}, axis=1)
        self.df = self.df.rename({3:"template_type_dicts3"}, axis=1)
        self.df = self.df.rename({4:"template_type_dicts4"}, axis=1)
        self.df = self.df.fillna(0)
        self.df = self.df.reset_index()
        
        if "template_type_dicts3" not in self.df.columns:
            self.df['template_type_dicts3'] = 0
        if "template_type_dicts4" not in self.df.columns:
            self.df['template_type_dicts4'] = 0
            
        # if "template_type_dicts3" in self.df.columns:
        #     self.df["template_type_dicts3"]=0
        # if "template_type_dicts4" in self.df.columns:
        #     self.df["template_type_dicts4"]=0
        # self.df.to_csv("template.csv")
    
        return self.df

    def create_candidates(self,df,df_graph):
        #self.df_graph.to_csv("df_graph_final.csv")
        count=0
        
        
        for rowIndex,row in self.df.iterrows():
            # print(row)
            for rowIndex1, row1 in self.df_merged.iterrows():
                # print(row1)
                print(row1["comparator_type"])
                measure_name=row1["Measure_Name"]
                oxcv=BNode(row1["Comparator_Node"][0])
        
                oq=BNode()
                count=count+1
        #print(row1)
                ah=BNode(row1["Comparator_Node"])
                ag=Literal(measure_name)
                self.a.add((self.sq12,self.pq12,oq) )
                self.a.add((oq,self.cp,self.co))
                a25=URIRef(row["text"])
                a27=URIRef(row["name"])
                a26=URIRef(row["display"])
                a28=URIRef(row["template_type_dicts"])
                a29=URIRef(row["template_type_dicts1"])
        
                self.a.add((oq,self.cp2,a25))
                self.a.add((oq,self.cp1,a27))
                self.a.add((oq,self.cp3,a26))
                self.a.add((oq,RDF.type,self.cp28))
                if(row["template_type_dicts"] != 0):
                    ov=BNode()
                    self.a.add((oq,self.cop4,ov))
                    self.a.add((ov,RDF.type,a28))
                if(row["template_type_dicts1"] != 0):
                    ov=BNode()
                    self.a.add((oq,self.cop4,ov))
                    self.a.add((ov,RDF.type,a29))
                if (row["template_type_dicts2"] != 0):
                    a30=URIRef(row["template_type_dicts2"])
                    ov=BNode()
                    self.a.add((oq,self.cop4,ov))
                    self.a.add((ov,RDF.type,a30))
                
                if (row["template_type_dicts3"] != 0):
                    a31=URIRef(row["template_type_dicts3"])
                    ov=BNode()
                    self.a.add((oq,self.cop4,ov))
                    self.a.add((ov,RDF.type,a31))
               
                if (row["template_type_dicts4"] != 0):
                    a32=URIRef(row["template_type_dicts4"])
                    ov=BNode()
                    self.a.add((oq,self.cop4,ov))
                    self.a.add((ov,RDF.type,a32))
                if "graph_type1" in self.df_graph.columns:
                    if (row1["graph_type1"] != 0):
                        a33=URIRef(row1["graph_type1"])
                        ov=BNode()
                        self.a.add((oq,self.cop4,ov))
                        self.a.add((ov,RDF.type,a33))
                        self.a.add((ov,self.cp23,ah))
                        self.a.add((ov,self.cp24,ag))
                if "graph_type2" in self.df_graph.columns:
                    if (row1["graph_type2"] != 0):
                        a34=URIRef(row1["graph_type2"])
                        ov=BNode()
                        self.a.add((oq,self.cop4,ov))
                        self.a.add((ov,RDF.type,a34))
                        self.a.add((ov,self.cp23,ah))
                        self.a.add((ov,self.cp24,ag))
                if "graph_type3" in self.df_graph.columns:
                    if (row1["graph_type3"] != 0):
                        a34=URIRef(row1["graph_type3"])
                        ov=BNode()
                        self.a.add((oq,self.cop4,ov))
                        self.a.add((ov,RDF.type,a34))
                        self.a.add((ov,self.cp23,ah))
                        self.a.add((ov,self.cp24,ag))
                if "graph_type4" in self.df_graph.columns:
                    if (row1["graph_type4"] != 0):
                        a34=URIRef(row1["graph_type4"])
                        ov=BNode()
                        self.a.add((oq,self.cop4,ov))
                        self.a.add((ov,RDF.type,a34))
                        self.a.add((ov,self.cp23,ah))
                        self.a.add((ov,self.cp24,ag))
                if "graph_type5" in self.df_graph.columns:
                    if (row1["graph_type5"] != 0):
                        a34=URIRef(row1["graph_type5"])
                        ov=BNode()
                        self.a.add((oq,self.cop4,ov))
                        self.a.add((ov,RDF.type,a34))
                        self.a.add((ov,self.cp23,ah))
                        self.a.add((ov,self.cp24,ag))
                if "graph_type6" in self.df_graph.columns:
                    if (row1["graph_type6"] != 0):
                        a34=URIRef(row1["graph_type6"])
                        ov=BNode()
                        self.a.add((oq,self.cop4,ov))
                        self.a.add((ov,RDF.type,a34))
                        self.a.add((ov,self.cp23,ah))
                        self.a.add((ov,self.cp24,ag))
                        a35=BNode("-p1")
                        self.a.add((oq,self.cp26,a35))
                        self.a36=URIRef(row["index"])
                        self.a.add((oq,self.cp27,self.a36))
                
                    
                #print(count)
        return self.a
            





        
        
                




