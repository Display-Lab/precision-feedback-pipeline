from typing import List, Tuple

import pytest
from rdflib import RDF, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from bitstomach2.signals import Comparison
from utils.namespace import PSDO, SLOWMO


@pytest.fixture
def perf_info() -> Tuple[Graph, Resource]:
    g = Graph()
    r = g.resource(BNode("performance_content"))
    r.set(RDF.type, PSDO.performance_content)
    return g, r

def test_comp_annotation_creates_minimal_subgraph():
    mi = Comparison()
    comparison = mi.detect({"levels": [0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89}})
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(mi, Graph)

    assert isinstance(comparison, List)
    assert isinstance(comparison[0], Resource)

    assert 2 == len(set(mi.subjects(RDF.type, PSDO.performance_gap_content)))


def test_node_is_aggregated_in_performance_info(perf_info):
    perf_graph, perf_content = perf_info
    signal = Comparison()

    # Create a small graph and return the base node(s) as a resource
    for s in signal.detect({"levels": [0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89}}):
        perf_content.add(URIRef("motivating_information"), s.identifier)

    # Add the remaining triples (the whole subgraph) to teh perf graph
    perf_graph += signal

    assert 15 == len(perf_graph)

    assert 2 == len(set(perf_graph.subjects(RDF.type, PSDO.performance_gap_content)))


def test_multiple_signals_from_single_detector(perf_info):
    perf_graph, perf_content = perf_info
    signal_graph = Comparison()

    signals = signal_graph.detect({"levels": [0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89}})

    assert 2 == len(signals)

    assert 12 == len(signal_graph)

    for s in signals:
        perf_content.add(URIRef("motivating_information"), s.identifier)

    perf_graph += signal_graph

    assert 15 == len(perf_graph)


def test_multiple_gap_values():
    signal = Comparison()

    pc = {"levels": [0.7, 0.8, 0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89, "peer_90th_percentile_benchmark":0.91, "goal_comparator_content":1.0}}

    signals = signal.detect(pc)

    assert 4 == len(signals)

    expected = [0.05, 0.01, -0.01, -0.1]

    for index, signal in enumerate(signals):
        v = signal.value(RDF.value).value
        assert pytest.approx(v) == expected[index]


def test_comparator_node():
    signal = Comparison()

    pc = {"levels": [0.7, 0.8, 0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89, "peer_90th_percentile_benchmark":0.91, "goal_comparator_content":1.0}}

    signals = signal.detect(pc)

    expected = [0.85, 0.89, 0.91, 1.0]
    
    for index, signal in enumerate(signals):
        assert Literal(expected[index]) == signal.value(SLOWMO.RegardingComparator / RDF.value)
        

def test_empty_performance_content_returns_value_error():
    mi = Comparison()
    with pytest.raises(ValueError): 
        mi.detect({})

    with pytest.raises(ValueError): 
        mi.detect({"comparators": {}})
        
    with pytest.raises(ValueError): 
        mi.detect({"levels": []})   
    
    with pytest.raises(IndexError):     
        mi.detect({"comparators": {}, "levels": []})   
         


    

    