from typing import List
import pytest
from rdflib import RDF, BNode, Graph, URIRef
from rdflib.resource import Resource
from utils.namespace import PSDO

from bitstomach2.signals import Comparison


@pytest.fixture
def perf_info() -> Graph:
    g = Graph()
    g.add(
        (BNode("PerformanceInformation"), RDF.type, URIRef("performance_information"))
    )
    assert 2 == len(g.all_nodes())
    return g


def test_comp_annotation_creates_minimal_subgraph():
    mi = Comparison()
    perf_data = {}

    expected_node = BNode("motivating_info")  # hard-coded for now

    comparison = mi.detect(perf_data)
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(mi, Graph)

    assert isinstance(comparison, List)
    assert isinstance(comparison[0], Resource)

    assert expected_node in mi.subjects(None, None)
    assert (expected_node, None, None) in mi

    assert (expected_node, RDF.type, PSDO.performance_gap_content) in mi


def test_node_is_aggregated_in_performance_info(perf_info):
    signal = Comparison()
    perf_data = {}
    performance_info = perf_info.resource(BNode("performance_info"))

    # Create a small graph and return the base node(s) as a resource
    for s in signal.detect(perf_data):
        performance_info.add(URIRef("motivating_information"), s.identifier)
        
    # Add the remaining triples (the whole subgraph) to teh perf graph
    perf_info += signal

    assert 7 == len(perf_info)

    assert (BNode("motivating_info"), RDF.type, PSDO.performance_gap_content) in perf_info


def test_multiple_signals_from_single_detector(perf_info):
    perf_data = {}
    performance_info = perf_info.resource(BNode("performance_info"))

    signal = Comparison()
    
    signals = signal.detect(perf_data)
    
    # for s in signal.detect(perf_data):
    #     performance_info.add(URIRef("motivating_information"), s.identifier)
    
    assert 2 == len(signals)
    
    assert 4 == len(signal)
    
    for s in signal.detect(perf_data):
        performance_info.add(URIRef("motivating_information"), s.identifier)

    perf_info += signal
    
    assert 7 == len(perf_info)
        
    


