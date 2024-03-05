from rdflib import BNode, Graph, RDF, URIRef
from bitstomach2 import bitstomach
from utils.namespace import PSDO

def test_extract_signals_return_a_graph():
    g = bitstomach.extract_signals({})
    
    assert isinstance(g, Graph) 
    
    assert g.value(None, RDF.type, PSDO.performance_content)
    

def test_returns_performance_content_with_multiple_elements():
    g = bitstomach.extract_signals([
['staff_number', 'measure', 'month', 'passed_count', 'flagged_count', 'denominator', 'peer_average_comparator', 'peer_75th_percentile_benchmark', 'peer_90th_percentile_benchmark', 'MPOG_goal'], 
[157, 'BP01', '2022-11-01', 29, 0, 29, 81.7, 100.0, 100.0, 90.0], 
[157, 'PONV05', '2022-11-01', 40, 0, 40, 82.4, 100.0, 100.0, 90.0]        
])
    r = g.resource(BNode("performance_content"))
    mi = set(r[URIRef("motivating_information")])
   
    # assert len(mi) == 2
    
    assert g.value(None, RDF.type, PSDO.performance_gap_content)
    
    
    
    