

from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF

#determine goal gaps exist
def goal_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['goal_comparison_value']
    goal_gap_size2=gap_size[0]

    gap_size=Normalize(gap_size,latest_measure_df['goal_comparison_value'])
    # print(gap_size)
    measure_name_node=BNode(latest_measure_df["measure"][0])
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))    
    performer_graph=annotate_goal_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_goal_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['goal_comparison_value'][0]<=latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_goal_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    if(latest_measure_df['goal_comparison_value'][0]>latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_goal_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    return performer_graph

#annotate goal gaps 
def annotate_goal_comparator(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000094')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph
#annotate performance goal gaps
def annotate_performance_goal_gap(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000106')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph
#annotate positive goal gap
def annotate_positive_goal_gap(performer_graph,blank_node,measure_Name,comparator_bnode,goal_gap_size,goal_gap_size2):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000104')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),goal_gap_size))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize2'),Literal(goal_gap_size2)))

    return performer_graph
#annotate negative goal gap
def annotate_negative_goal_gap(performer_graph,blank_node,measure_Name,comparator_bnode,goal_gap_size,goal_gap_size2):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),goal_gap_size))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize2'),Literal(goal_gap_size2)))

    return performer_graph
#determine peer gaps exist
def peer_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_average_comparator']
    peer_gap_size2=gap_size[0]

    gap_size=Normalize(gap_size,latest_measure_df['peer_average_comparator'])
    # print(gap_size)
    measure_name_node=BNode(latest_measure_df["measure"][0])
    peer_gap_size=gap_size[0]
    peer_gap_size=Literal(peer_gap_size)
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
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,peer_gap_size,peer_gap_size2)
    if(latest_measure_df['Performance_Rate'][0]<latest_measure_df['peer_average_comparator'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,peer_gap_size,peer_gap_size2)
    return performer_graph

#annotate peer top 10 gaps 
def annotate_top_10_percentile(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000129')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

#determine top 10 gaps exists
def top_10_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_90th_percentile_benchmark']
    goal_gap_size2=gap_size[0]
    gap_size=Normalize(gap_size,latest_measure_df['peer_90th_percentile_benchmark'])
    measure_name_node=BNode(latest_measure_df["measure"][0])
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_peer_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    performer_graph=annotate_top_10_percentile(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
    # performer_graph=annotate_top_10_percentile(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['peer_90th_percentile_benchmark'][0]<=latest_measure_df['Performance_Rate'][0]):
        # print("entere here")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    if(latest_measure_df['peer_90th_percentile_benchmark'][0]==latest_measure_df['Performance_Rate'][0]):
            # print("entere here")
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    if(latest_measure_df['Performance_Rate'][0]<latest_measure_df['peer_90th_percentile_benchmark'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    return performer_graph

#annotate top 25 gaps 
def annotate_top_25_percentile(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000128')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

#determine top 25 gaps exists
def top_25_gap_annotate(performer_graph,p1_node,latest_measure_df,comparator_bnode):
    latest_measure_df=latest_measure_df.reset_index(drop=True)
    gap_size=latest_measure_df['Performance_Rate']-latest_measure_df['peer_75th_percentile_benchmark']
    goal_gap_size2=gap_size[0]
    gap_size=Normalize(gap_size,latest_measure_df['peer_90th_percentile_benchmark'])
    # print(gap_size)
    measure_name_node=BNode(latest_measure_df["measure"][0])
    goal_gap_size=gap_size[0]
    goal_gap_size=Literal(goal_gap_size)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_peer_comparator(performer_graph,blank_node,measure_name_node,comparator_bnode)
    performer_graph=annotate_top_25_percentile(performer_graph,blank_node,measure_name_node,comparator_bnode)
    blank_node=BNode() 
    performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
    performer_graph=annotate_performance_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode)
    #performer_graph=annotate_top_25_percentile(performer_graph,blank_node,measure_name_node,comparator_bnode)
    if(latest_measure_df['peer_75th_percentile_benchmark'][0]<=latest_measure_df['Performance_Rate'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_positive_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    if(latest_measure_df['Performance_Rate'][0]<latest_measure_df['peer_75th_percentile_benchmark'][0]):
        blank_node=BNode() 
        performer_graph.add((p1_node,URIRef('http://purl.obolibrary.org/obo/RO_0000091'),blank_node))
        performer_graph=annotate_negative_peer_gap(performer_graph,blank_node,measure_name_node,comparator_bnode,goal_gap_size,goal_gap_size2)
    return performer_graph

def Normalize(gap_size,max_value):
    # x=[-1,1]
    gap_size=abs(gap_size)
    x1=(2*((gap_size-0)/((max_value*100)-0)))-1
    # print(gap_size)
    # print(max_value*100)
    print("normalized value")
    print(x1)
    return x1
#annotate peer comparator
def annotate_peer_comparator(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000095')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph
#annotate peer average comparator
def annotate_peer_average_comparator(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000126')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph
#annotate performance peer gap comparator
def annotate_performance_peer_gap(performer_graph,blank_node,measure_Name,comparator_bnode):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000106')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    return performer_graph

#annotate positive peer gap 
def annotate_positive_peer_gap(performer_graph,blank_node,measure_Name,comparator_bnode,peer_gap_size,peer_gap_size2):
    # print("entered here")
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000104')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),peer_gap_size))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize2'),Literal(peer_gap_size2)))
    
    return performer_graph

#annotate negative peer gap
def annotate_negative_peer_gap(performer_graph,blank_node,measure_Name,comparator_bnode,peer_gap_size,peer_gap_size2):
    performer_graph.add((blank_node,RDF.type,URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),comparator_bnode))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),measure_Name))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize'),peer_gap_size))
    performer_graph.add((blank_node,URIRef('http://example.com/slowmo#PerformanceGapSize2'),Literal(peer_gap_size2)))
    
    return performer_graph