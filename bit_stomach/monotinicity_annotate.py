

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF


def monotonic_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    back_up_df=latest_measure_df
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(3) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    m1=latest_measure_df["Performance_Rate"][1]-latest_measure_df["Performance_Rate"][0]
    m2=latest_measure_df["Performance_Rate"][2]-latest_measure_df["Performance_Rate"][1]
    if(m1>0 and m2 <0)or(m1<0 and m2>0):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_non_monotonic_trend(performer_graph,blank_node,measure_name_node,comparator_bnode)
        
    if(m1>0 and m2>0) or (m1<0 and m2<0):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode()
        if(m1>0 and m2>0):
            intervals= find_number(back_up_df,"positive")
        if(m1<0 and m2<0):
            intervals= find_number(back_up_df,"negative")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_monotonic_trend(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
            
    #back_up_df.to_csv('slope22.csv')
    #print(trend_sign)
    return performer_graph

def annotate_non_monotonic_trend(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://example.com/slowmo#NonMonotonicTrend')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph
def annotate_monotonic_trend(performer_graph,blank_node,measure_Name,comparator_bnode,intervals):
    performer_graph.add((blank_node,RDF.type,URIRef('http://example.com/slowmo#MonotonicTrend')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#Timeofmonotonicity'),Literal(intervals)))
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