import sys
import sys
import warnings
import time
import logging
import json
import re
import numpy as np 
import matplotlib.pyplot as plt 
import scipy
from scipy import stats
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



def trend_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    back_up_df=latest_measure_df
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    idx= latest_measure_df.groupby(['Measure_Name'])['Month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    trend_sign=latest_measure_df["Performance_Rate"][1]-latest_measure_df["Performance_Rate"][0]
    #back_up_df.to_csv('slope22.csv')
    #print(trend_sign)
    if trend_sign<0:
        ac=BNode(latest_measure_df["Measure_Name"][0])
        av=comparator_bnode

    #         #annotate goal comparator
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        #input_graph=annotate_goal_negative_trend(input_graph,o14,ac,av)
        trend_sign1="negative"
        number=find_number(back_up_df,trend_sign1)
        idx= back_up_df.groupby(['Measure_Name'])['Month'].nlargest(number) .reset_index()
        l=idx['level_1'].tolist()
        measure_df =  back_up_df[back_up_df.index.isin(l)]
        out = latest_measure_df.groupby('Measure_Name').apply(theil_reg, xcol='Month', ycol='Performance_Rate')
        df_1=out[0]
        df_1 = df_1.reset_index()
        df_1 = df_1.rename({0:"performance_trend_slope"}, axis=1)
        
        trend_slope=df_1["performance_trend_slope"][0]
        
        # print(trend_slope)
        # print(number)
        input_graph=annotate_negative_trend(input_graph,o14,ac,av,trend_slope,number)

    if trend_sign>0:
        ac=BNode(latest_measure_df["Measure_Name"][0])
        av=comparator_bnode
      
    #         #annotate goal comparator
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        trend_sign1="positive"
        number=find_number(back_up_df,trend_sign1)
        idx= back_up_df.groupby(['Measure_Name'])['Month'].nlargest(number) .reset_index()
        l=idx['level_1'].tolist()
        measure_df =  back_up_df[back_up_df.index.isin(l)]
        out = latest_measure_df.groupby('Measure_Name').apply(theil_reg, xcol='Month', ycol='Performance_Rate')
        df_1=out[0]
        df_1 = df_1.reset_index()
        df_1 = df_1.rename({0:"performance_trend_slope"}, axis=1)
        
        trend_slope=df_1["performance_trend_slope"][0]
        input_graph=annotate_positive_trend(input_graph,o14,ac,av,trend_slope,number)
     
    #a=insert_annotate(input_graph)
    
   

    

    return input_graph

def annotate_negative_trend(a,s16,measure_Name,o16,trend_slope,number):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000100')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    trend_slope=Literal(trend_slope)
    number=Literal(number)
    p18=URIRef('http://example.com/slowmo#PerformanceTrendSlope')
    o18=trend_slope
    a.add((s16,p18,o18))
    p18=URIRef('http://example.com/slowmo#numberofmonths')
    o18=number
    a.add((s16,p18,o18))
    return a

def annotate_positive_trend(a,s16,measure_Name,o16,trend_slope,number):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/psdo_0000099')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    trend_slope=Literal(trend_slope)
    number=Literal(number)
    p18=URIRef('http://example.com/slowmo#PerformanceTrendSlope')
    o18=trend_slope
    a.add((s16,p18,o18))
    p18=URIRef('http://example.com/slowmo#numberofmonths')
    o18=number
    a.add((s16,p18,o18))
    return a


def find_number(backup_df,trend_sign1):
    if(trend_sign1=="negative"):
        x=2
        lista=[]
        lista=backup_df["Performance_Rate"].tolist()
        count=0
        y=-1
        z=y-1
        for x in range(len(lista)):
            if lista[z]<=lista[y]:
                return count
            if(lista[z]>lista[y]):
                count=count+1
                y=y-1
                z=y-1
        return count
    if(trend_sign1=="positive"):
        x=2
        lista=[]
        lista=backup_df["Performance_Rate"].tolist()
        count=0
        y=-1
        z=y-1
        for x in range(len(lista)):
            if lista[z]>=lista[y]:
                return count
            if(lista[z]<lista[y]):
                count=count+1
                y=y-1
                z=y-1
        return count

def theil_reg(df, xcol, ycol):

   model = stats.theilslopes(df[ycol],df[xcol])
   return pd.Series(model)

