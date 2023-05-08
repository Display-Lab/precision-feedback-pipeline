 

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector

s=URIRef("http://example.com/app#display-lab")
p=URIRef('http://example.com/slowmo#IsAboutMeasure')

def goal_acheivementloss_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['goal_comparison_value']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    
    if((latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        av=comparator_bnode
        o14=BNode() 
        event="loss"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_loss(input_graph,o14,ac,av,number)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        av=comparator_bnode
        o14=BNode() 
        event="acheivement"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_acheivement(input_graph,o14,ac,av,number)



    #print(latest_measure_df)
    return input_graph

def annotate_loss(performer_graph,performance_content_node,measure_name_node,comparator_node,intervals):
    
    performer_graph.add(
        (performance_content_node,
        RDF.type,
        URIRef('http://purl.obolibrary.org/obo/PSDO_0000113')))#loss content
    
    performer_graph.add(
        (performance_content_node,
         URIRef('http://example.com/slowmo#RegardingComparator'),
         comparator_node))
    
    performer_graph.add(
        (performance_content_node,
         URIRef('http://example.com/slowmo#RegardingMeasure'),
         measure_name_node))
    
    performer_graph.add(
        (performance_content_node,
         URIRef('http://example.com/slowmo#TimeSinceLastAcheivement'),
         Literal(intervals)))
    return performer_graph

def annotate_acheivement(a,s16,measure_Name,o16,number):
    p15=RDF.type
    o15=URIRef('http://purl.obolibrary.org/obo/PSDO_0000112')
    a.add((s16,p15,o15))
    p16=URIRef('http://example.com/slowmo#RegardingComparator')
    a.add((s16,p16,o16))
    p17=URIRef('http://example.com/slowmo#RegardingMeasure')
    o17=measure_Name
    a.add((s16,p17,o17))
    p18=URIRef('http://example.com/slowmo#TimeSinceLastLoss')
    o18=Literal(number)
    a.add((s16,p18,o18))
    return a

def peer_acheivementloss_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_average_comparator']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
   
    # print(latest_measure_df)
    if((latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        ac=BNode(latest_measure_df["measure"][0]) #measure name "FLUID_01"
        av=comparator_bnode
        o14=BNode() 
        event="loss"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_loss(input_graph,o14,ac,av,number)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        
        av=comparator_bnode
        o14=BNode() 
        event="acheivement"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_acheivement(input_graph,o14,ac,av,number)



    #print(latest_measure_df)
    return input_graph

def top_10_acheivementloss_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_90th_percentile_benchmark']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    
    # print(latest_measure_df)
    if((latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        av=comparator_bnode
        o14=BNode() 
        event="loss"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_loss(input_graph,o14,ac,av,number)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        
        av=comparator_bnode
        o14=BNode() 
        event="acheivement"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_acheivement(input_graph,o14,ac,av,number)



    #print(latest_measure_df)
    return input_graph
def top_25_acheivementloss_annotate(input_graph,s13,latest_measure_df,comparator_bnode):
    
    s14=s13
    p14=URIRef('http://purl.obolibrary.org/obo/RO_0000091')
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_75th_percentile_benchmark']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(2) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    
    #print(latest_measure_df)
    if((latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        av=comparator_bnode
        o14=BNode() 
        event="loss"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_loss(input_graph,o14,ac,av,number)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        ac=BNode(latest_measure_df["measure"][0])
        
        av=comparator_bnode
        o14=BNode() 
        event="acheivement"
        number=find_number(back_up_df,event)
        input_graph.add((s14,p14,o14))
        input_graph=annotate_acheivement(input_graph,o14,ac,av,number)



    #print(latest_measure_df)
    return input_graph


def find_number(backup_df,trend_sign1):
    if(trend_sign1=="loss"):
        
        lista=[]
        lista=backup_df["goal_gap_size"].tolist()
        count=1
        y=-1
        
        for x in range(len(lista)):
            if lista[y]>0:
                return count
            if(lista[y]<0):
                count=count+1
                y=y-1
                
        return count
    if(trend_sign1=="acheivement"):
        
        lista=[]
        lista=backup_df["goal_gap_size"].tolist()
        count=1
        y=-1
        
        for x in range(len(lista)):
            if lista[y]<0:
                return count
            if(lista[y]>0):
                count=count+1
                y=y-1
                
        return count