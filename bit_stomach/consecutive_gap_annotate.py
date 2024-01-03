
from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector


def goal_consecutive_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['goal_comparison_value']-latest_measure_df['Performance_Rate']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(3) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
 
    if((latest_measure_df["goal_gap_size"][2]>0 and latest_measure_df["goal_gap_size"][1]>0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        blank_node=BNode() 
        intervals=find_number(back_up_df,"positive")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_goal_positive_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][2]<0 and latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        intervals=find_number(back_up_df,"negative")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_goal_negative_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph

def peer_consecutive_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
   
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['peer_average_comparator']-latest_measure_df['Performance_Rate']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(3) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    # print(latest_measure_df)
    # print(latest_measure_df["goal_gap_size"][1])
    if((latest_measure_df["goal_gap_size"][2]>0 and latest_measure_df["goal_gap_size"][1]>0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"positive")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_peer_positive_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][2]<0 and latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        
        intervals=find_number(back_up_df,"negative")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_peer_negative_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph

def top_10_consecutive_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['peer_90th_percentile_benchmark']-latest_measure_df['Performance_Rate']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(3) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    # print(latest_measure_df)
    # print(latest_measure_df["goal_gap_size"][1])
    if((latest_measure_df["goal_gap_size"][2]>0 and latest_measure_df["goal_gap_size"][1]>0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
       
        intervals=find_number(back_up_df,"positive")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_peer_positive_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][2]<0 and latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        
        intervals=find_number(back_up_df,"negative")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_peer_negative_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph
def top_25_consecutive_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
   
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    goal_gap_size=[]
    goal_gap_size=latest_measure_df['peer_75th_percentile_benchmark']-latest_measure_df['Performance_Rate']
    latest_measure_df["goal_gap_size"]=goal_gap_size
    back_up_df=latest_measure_df
    idx= latest_measure_df.groupby(['measure'])['month'].nlargest(3) .reset_index()
    l=idx['level_1'].tolist()
    latest_measure_df =  latest_measure_df[latest_measure_df.index.isin(l)]
    latest_measure_df = latest_measure_df.reset_index(drop=True)
    # print(latest_measure_df)
    # print(latest_measure_df["goal_gap_size"][1])
    if((latest_measure_df["goal_gap_size"][2]>0 and latest_measure_df["goal_gap_size"][1]>0 and latest_measure_df["goal_gap_size"][0]>=0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"positive")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_peer_positive_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][2]<0 and latest_measure_df["goal_gap_size"][1]<0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        
        intervals=find_number(back_up_df,"negative")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_consecutive_peer_negative_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph


def annotate_consecutive_goal_positive_gap(performer_graph,blank_node,measure_Name,comparator_bnode,intervals):
    performer_graph.add((blank_node,RDF.type,URIRef('http://example.com/slowmo#ConsecutiveGoalPositiveGap')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#Numberofmonths'),Literal(intervals)))
    return performer_graph


def annotate_consecutive_goal_negative_gap(performer_graph,blank_node,measure_Name,comparator_bnode,intervals):
    performer_graph.add((blank_node,RDF.type,URIRef('http://example.com/slowmo#ConsecutiveGoalNegativeGap')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#Numberofmonths'),Literal(intervals)))
    return performer_graph

def annotate_consecutive_peer_positive_gap(performer_graph,blank_node,measure_Name,comparator_bnode,intervals):
    
    performer_graph.add((blank_node,RDF.type,URIRef('http://example.com/slowmo#ConsecutivePeerPositiveGap')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#Numberofmonths'),Literal(intervals)))
    return performer_graph
    

def annotate_consecutive_peer_negative_gap(performer_graph,blank_node,measure_Name,comparator_bnode,intervals):
    performer_graph.add((blank_node,RDF.type,URIRef('http://example.com/slowmo#ConsecutivePeerNegativeGap')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#Numberofmonths'),Literal(intervals)))
    return performer_graph    

def find_number(backup_df,trend_sign1):
    if(trend_sign1=="negative"):
        
        lista=[]
        lista=backup_df["goal_gap_size"].tolist()
        count=0
        y=-1
        
        for x in range(len(lista)):
            if lista[y]>0:
                return count
            if(lista[y]<0):
                count=count+1
                y=y-1
                
        return count
    if(trend_sign1=="positive"):
        
        lista=[]
        lista=backup_df["goal_gap_size"].tolist()
        count=0
        y=-1
        
        for x in range(len(lista)):
            if lista[y]<0:
                return count
            if(lista[y]>0):
                count=count+1
                y=y-1
                
        return count