
from scipy import stats
import pandas as pd
from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF
#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector





def trend_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    # print(latest_measure_df)

    back_up_df=latest_measure_df
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    trend_sign=latest_measure_df["Performance_Rate"][1]-latest_measure_df["Performance_Rate"][0]
    
    # trend_slope must match the sign of trend_sign, e.g. if this month was positive we can't report a negative trend slope for 3 month
    trend_slope = back_up_df.groupby('measure').apply(calculate_trend,'month', 'Performance_Rate')[0]
    
    if trend_sign<0:
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        intervals=find_number(back_up_df,"negative")
        idx= back_up_df.groupby(['measure'])['month'].nlargest(intervals) .reset_index()
        l=idx['level_1'].tolist()
        performer_graph=annotate_negative_trend(performer_graph,blank_node,measure_name_node,comparator_bnode,trend_slope,intervals)

    if trend_sign>0:
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        intervals=find_number(back_up_df,"positive")
        idx= back_up_df.groupby(['measure'])['month'].nlargest(intervals) .reset_index()
        l=idx['level_1'].tolist()
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
#    print(pd.Series(model))
   return pd.Series(model)

def calculate_trend(df, month, performance_rate):
    performance_rates = list(df[performance_rate])
    last_index= len(performance_rates) - 1 
    change_this_month = performance_rates[last_index ] - performance_rates[last_index - 1]
    change_last_month = performance_rates[last_index - 1] - performance_rates[last_index - 2]
    
    if change_this_month * change_last_month < 0:
        return 0   
    
    return (performance_rates[last_index ] - performance_rates[last_index - 2]) / 2
    
    