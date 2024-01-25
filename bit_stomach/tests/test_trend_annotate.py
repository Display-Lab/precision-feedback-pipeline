import unittest
from unittest.mock import Mock
import trend_annotate
import pandas as pd
import json
import rdflib
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.serializer import Serializer
from operator import itemgetter
import itertools
import collections



class Trend_annotateTestcase(unittest.TestCase):

    def test_find_number(self):
        #create test data
        #test data1
        back_up_df= pd.DataFrame(columns=['measure', 'month', 'peer_average_comparator',
        'peer_90th_percentile_benchmark', 'peer_75th_percentile_benchmark',
        'Performance_Rate', 'goal_comparison_value'], 
                    index = [1, 2, 3])
        back_up_df.loc[1] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
        back_up_df.loc[2] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
        back_up_df.loc[3] = ["BP03","2023-12-01",85,88,96,0.85,0.90]
        #test data2
        back_up_df1= pd.DataFrame(columns=['measure', 'month', 'peer_average_comparator',
        'peer_90th_percentile_benchmark', 'peer_75th_percentile_benchmark',
        'Performance_Rate', 'goal_comparison_value'], 
                    index = [1, 2, 3])
        back_up_df1.loc[1] = ["BP03","2023-11-01",85,88,96,0.80,0.90]
        back_up_df1.loc[2] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
        back_up_df1.loc[3] = ["BP03","2023-12-01",85,88,96,0.95,0.90]
        #testdata3
        back_up_df2= pd.DataFrame(columns=['measure', 'month', 'peer_average_comparator',
        'peer_90th_percentile_benchmark', 'peer_75th_percentile_benchmark',
        'Performance_Rate', 'goal_comparison_value'], 
                    index = [1, 2, 3])
        back_up_df2.loc[1] = ["BP03","2023-11-01",85,88,96,0.90,0.90]
        back_up_df2.loc[2] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
        back_up_df2.loc[3] = ["BP03","2023-12-01",85,88,96,0.80,0.90]

        #test
        assert trend_annotate.find_number(back_up_df,"positive") == 0
        assert trend_annotate.find_number(back_up_df1,"positive") == 2
        assert trend_annotate.find_number(back_up_df2,"negative") == 2

    def test_annotate_positive_trend(self):
        #create test data
        file_json=open("./bit_stomach/tests/tests_inputs/trend_positive_test.json")
        file_json1=json.load(file_json)
        performergraphjson=json.dumps(file_json1)
        performer_graph = Graph()
        performer_graph.parse(data=performergraphjson,format="json-ld")
        blank_node=BNode("_:Nef4605383e534edb90633a3c30587157")
        measure_Name=Literal("_:BP03")
        comparator_bnode=BNode("_:N23cd5c14a87644ac9b3366bae5213861")
        trend_slope=1.1574074074074085e-17
        intervals=2

        #call method of test
        Resultant_graph=trend_annotate.annotate_positive_trend(performer_graph,blank_node,measure_Name,comparator_bnode,trend_slope,intervals)
        for s,p,o in Resultant_graph.triples((blank_node,URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),None)):
            Resultant_positive_annotation=str(o)
        for s,p,o in Resultant_graph.triples((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),None)):
            Resultant_comparator_node= str(o)
        for s,p,o in Resultant_graph.triples((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),None)):
            Resultant_Measure= str(o)
        for s,p,o in Resultant_graph.triples((blank_node,URIRef('http://example.com/slowmo#PerformanceTrendSlope'),None)):
            Resultant_Trend_slope= str(o)
        for s,p,o in Resultant_graph.triples((blank_node,URIRef('http://example.com/slowmo#numberofmonths'),None)):
            Resultant_Intervals= str(o)

        #converting resultant graph to json object
        Resultant_graph_json=Resultant_graph.serialize(format='json-ld', indent=4)
        #writing resultant output
        f = open("./bit_stomach/tests/test_outputs/Trend_positive_output.json", "w")
        f.write(Resultant_graph_json)
        f.close()


        #loading expected output
        file_json1=open("./bit_stomach/tests/expected_tests_outputs/expected_trend_positive_test.json")
        expected_graph_json=json.load(file_json1)
        expected_graphjson=json.dumps(expected_graph_json)
        expected_graph = Graph()
        expected_graph.parse(data=expected_graphjson,format="json-ld")
        # expected_graph_json_list=list(itertools.chain.from_iterable(expected_graph_json))
        for s,p,o in expected_graph.triples((blank_node,URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),None)):
            Expected_positive_annotation=str(o)
        for s,p,o in expected_graph.triples((blank_node,URIRef('http://example.com/slowmo#RegardingComparator'),None)):
            Expected_comparator_node= str(o)
        for s,p,o in expected_graph.triples((blank_node,URIRef('http://example.com/slowmo#RegardingMeasure'),None)):
            Expected_Measure= str(o)
        for s,p,o in expected_graph.triples((blank_node,URIRef('http://example.com/slowmo#PerformanceTrendSlope'),None)):
            Expected_Trend_slope= str(o)
        for s,p,o in expected_graph.triples((blank_node,URIRef('http://example.com/slowmo#numberofmonths'),None)):
            Expected_Intervals= str(o)
        
        #assert if positive trend annotation is added
        assert Expected_positive_annotation == Resultant_positive_annotation
        #assert if comparator_node is added correctly
        assert Expected_comparator_node == Resultant_comparator_node
        #assert if Measure is added correctly
        assert Expected_Measure == Resultant_Measure
        #assert if trend slope is added correctly
        assert Expected_Trend_slope == Resultant_Trend_slope
        #assert if intervals is added correctly
        assert Resultant_Intervals == Expected_Intervals

 