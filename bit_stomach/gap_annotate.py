

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF

def goal_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['goal_comparison_value']
    # if (gap_size[0]!= 0):
    measure_name_node=BNode(latest_measure_df["measure"][0])
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    #         #annotate goal comparator
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_goal_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_goal_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['goal_comparison_value'][0]<=latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_goal_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    if(latest_measure_df['goal_comparison_value'][0]>latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_goal_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    return performer_graph

def annotate_goal_comparator(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000094')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

def annotate_performance_goal_gap(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000106')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

def annotate_positive_goal_gap(performer_graph,blank_node,measure_Name,comparator_bnode,goal_gap_size):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000104')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),goal_gap_size))
    return performer_graph

def annotate_negative_goal_gap(performer_graph,blank_node,measure_Name,comparator_bnode,goal_gap_size):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),goal_gap_size))
    return performer_graph

def peer_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_average_comparator']
    measure_name_node=BNode(latest_measure_df["measure"][0])
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    #         #annotate goal comparator
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_peer_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    performer_graph=annotate_peer_average_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['peer_average_comparator'][0]<=latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    if(latest_measure_df['Performance_Rate'][0]<latest_measure_df['peer_average_comparator'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    return performer_graph



def annotate_top_10_percentile(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000129')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph


def top_10_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_90th_percentile_benchmark']
    measure_name_node=BNode(latest_measure_df["measure"][0])
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_peer_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    performer_graph=annotate_peer_average_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
        # o14=BNode()
        
    performer_graph=annotate_top_10_percentile(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['peer_90th_percentile_benchmark'][0]<=latest_measure_df['Performance_Rate'][0]):
        # print("entere here")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    if(latest_measure_df['peer_90th_percentile_benchmark'][0]==latest_measure_df['Performance_Rate'][0]):
            # print("entere here")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    if(latest_measure_df['Performance_Rate'][0]<latest_measure_df['peer_90th_percentile_benchmark'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    return performer_graph

def annotate_top_25_percentile(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000128')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

def top_25_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    
    
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    
    
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_75th_percentile_benchmark']
    
    # if (gap_size[0]>= 0):
    measure_name_node=BNode(latest_measure_df["measure"][0])
    
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    #         #annotate goal comparator
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_peer_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    performer_graph=annotate_peer_average_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
        # o14=BNode()
        
    performer_graph=annotate_top_25_percentile(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['peer_75th_percentile_benchmark'][0]<=latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        # print("entered annotation")
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
    if(latest_measure_df['Performance_Rate'][0]<latest_measure_df['peer_75th_percentile_benchmark'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size)
        

    

    return performer_graph

def annotate_peer_comparator(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000095')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

def annotate_peer_average_comparator(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000126')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

def annotate_performance_peer_gap(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000106')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

def annotate_positive_peer_gap(performer_graph,blank_node,measure_Name,comparator_bnode,goal_gap_size):
    # print("entered here")
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000104')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),goal_gap_size))
    return performer_graph

def annotate_negative_peer_gap(performer_graph,blank_node,measure_Name,comparator_bnode,goal_gap_size):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),goal_gap_size))
    return performer_graph