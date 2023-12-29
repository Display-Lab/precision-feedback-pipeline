 

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector


#calculate goal/acheivement loss annontate
def goal_acheivementloss_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
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
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"loss")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_loss(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"acheivement")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_acheivement(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph
#calculate loss annotate
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
#calculate  acheivement annotate
def annotate_acheivement(performer_graph,performance_content_node,measure_Name,comparator_node,intervals):
    performer_graph.add((performance_content_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000112')))
    performer_graph.add((performance_content_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_node))
    performer_graph.add((performance_content_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((performance_content_node,URIRef('http://example.com/slowmo#TimeSinceLastLoss'),Literal(intervals)))
    return performer_graph
#calculate peer acheivement_loss_annotate
def peer_acheivementloss_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
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
        measure_name_node=BNode(latest_measure_df["measure"][0]) #measure name "FLUID_01"
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"loss")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_loss(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"acheivement")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_acheivement(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph
#calculate top10 acheivement_loss_annotate
def top_10_acheivementloss_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
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
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"loss")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_loss(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
       
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"acheivement")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_acheivement(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph
#calculate top25 acheivement_loss_annotate
def top_25_acheivementloss_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
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
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"loss")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_loss(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)
    if((latest_measure_df["goal_gap_size"][1]>=0 and latest_measure_df["goal_gap_size"][0]<0)==True):
        measure_name_node=BNode(latest_measure_df["measure"][0])
        
        
        blank_node=BNode() 
        
        intervals=find_number(back_up_df,"acheivement")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_acheivement(performer_graph,blank_node,measure_name_node,comparator_bnode,intervals)



    #print(latest_measure_df)
    return performer_graph


#calculate intervals of acheivement and loss
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