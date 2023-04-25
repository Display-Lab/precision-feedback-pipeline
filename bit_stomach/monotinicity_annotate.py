

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF


def monotonic_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    back_up_df=latest_measure_df
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(3) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    m1=latest_measure_df["Performance_Rate"][1]-latest_measure_df["Performance_Rate"][0]
    m2=latest_measure_df["Performance_Rate"][2]-latest_measure_df["Performance_Rate"][1]
    if(m1>0 and m2 <0)or(m1<0 and m2>0):
        ac=BNode(latest_measure_df["measure"][0])
        av=comparator_bnode
        o14=BNode() 
        input_graph.add((s14,p14,o14))
        input_graph=annotate_non_monotonic_trend(input_graph,o14,ac,av)
        
    if(m1>0 and m2>0) or (m1<0 and m2<0):
        ac=BNode(latest_measure_df["measure"][0])
        av=comparator_bnode
        o14=BNode()
        if(m1>0 and m2>0):
            mono="positive"
            number= find_number(back_up_df,mono)
        if(m1<0 and m2<0):
            mono="negative"
            number= find_number(back_up_df,mono)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_monotonic_trend(input_graph,o14,ac,av,number)
            
    #back_up_df.to_csv('slope22.csv')
    #print(trend_sign)
    return input_graph

def annotate_non_monotonic_trend(a,s16,measure_Name,o16):
    p15=RDF.type
    o15=URIRef('http://example.com/slowmo#NonMonotonicTrend')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    # p18=URIRef('http://example.com/slowmo#TimeSinceLastAcheivement')
    # o18=Literal(number)
    # a.add((s16,p18,o18))
    return a
def annotate_monotonic_trend(a,s16,measure_Name,o16,number):
    p15=RDF.type
    o15=URIRef('http://example.com/slowmo#MonotonicTrend')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    p18=URIRef('http://example.com/slowmo#Timeofmonotonicity')
    o18=Literal(number)
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