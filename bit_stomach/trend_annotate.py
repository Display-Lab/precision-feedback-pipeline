
from scipy import stats
import pandas as pd
from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector





def trend_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    back_up_df=latest_measure_df
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    trend_sign=latest_measure_df["Performance_Rate"][1]-latest_measure_df["Performance_Rate"][0]
    
    if trend_sign<0:
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        intervals=find_number(back_up_df,"negative")
        idx= back_up_df.groupby(['measure'])['month'].nlargest(intervals) .reset_index()
        l=idx['level_1'].tolist()
        measure_df =  back_up_df[back_up_df.index.isin(l)]
        out = latest_measure_df.groupby('measure').apply(theil_reg, xcol='month', ycol='Performance_Rate')
        df_1=out[0]
        df_1 = df_1.reset_index()
        df_1 = df_1.rename({0:"performance_trend_slope"}, axis=1)
        trend_slope=df_1["performance_trend_slope"][0]
        performer_graph=annotate_negative_trend(performer_graph,blank_node,measure_name_node,comparator_bnode,trend_slope,intervals)

    if trend_sign>0:
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        intervals=find_number(back_up_df,"positive")
        idx= back_up_df.groupby(['measure'])['month'].nlargest(intervals) .reset_index()
        l=idx['level_1'].tolist()
        measure_df =  back_up_df[back_up_df.index.isin(l)]
        out = latest_measure_df.groupby('measure').apply(theil_reg, xcol='month', ycol='Performance_Rate')
        df_1=out[0]
        df_1 = df_1.reset_index()
        df_1 = df_1.rename({0:"performance_trend_slope"}, axis=1)
        trend_slope=df_1["performance_trend_slope"][0]
        performer_graph=annotate_positive_trend(performer_graph,blank_node,measure_name_node,comparator_bnode,trend_slope,intervals)
    return performer_graph

def annotate_negative_trend(performer_graph,blank_node,measure_Name,comparator_bnode,trend_slope,intervals):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000100')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceTrendSlope'),Literal(trend_slope)))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#numberofmonths'),Literal(intervals)))
    return performer_graph

def annotate_positive_trend(performer_graph,blank_node,measure_Name,comparator_bnode,trend_slope,intervals):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000099')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceTrendSlope'),Literal(trend_slope)))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#numberofmonths'),Literal(intervals)))
    return performer_graph


def find_number(backup_df,trend_sign1):
    if(trend_sign1=="negative"):
        x=2
        lista=[]
        lista=backup_df["Performance_Rate"].tolist()
        count=0
        y=-1
        z=y-1
        for x in range(len(lista)-1):
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
        for x in range(len(lista)-1):
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

