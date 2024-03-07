from typing import List, Tuple
import pandas as pd

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

@pytest.fixture
def perf_data() -> pd.DataFrame:
    performance_data = [[ "staff_number", "measure", "month", "passed_percentage", "passed_count", "flagged_count", "denominator", "peer_average_comparator", "peer_75th_percentile_benchmark", "peer_90th_percentile_benchmark", "goal_comparator_content" ],
  [157, "BP01", "2022-08-01", 85.0, 85.0, 0, 100.0, 84.0, 88.0, 90.0, 99.0],
  [157, "BP01", "2022-09-01", 90.0, 90.0, 0, 100.0, 85.0, 89.0, 91.0, 100.0]]
    return pd.DataFrame(performance_data[1:], columns=performance_data[0])

def test_comp_annotation_creates_minimal_subgraph(perf_data):
    mi = Comparison()

    comparison = mi.detect(perf_data)
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(mi, Graph)

    assert isinstance(comparison, List)
    assert isinstance(comparison[0], Resource)

    assert 4 == len(set(mi.subjects(RDF.type, PSDO.performance_gap_content)))


def test_node_is_aggregated_in_performance_info(perf_info, perf_data):
    perf_graph, perf_content = perf_info
    signal = Comparison()

    # Create a small graph and return the base node(s) as a resource
    for s in signal.detect(perf_data):
        perf_content.add(URIRef("motivating_information"), s.identifier)

    # Add the remaining triples (the whole subgraph) to teh perf graph
    perf_graph += signal

    assert 33 == len(perf_graph)

    assert 4 == len(set(perf_graph.subjects(RDF.type, PSDO.performance_gap_content)))


def test_multiple_signals_from_single_detector(perf_info, perf_data):
    perf_graph, perf_content = perf_info
    signal_graph = Comparison()

    signals = signal_graph.detect(perf_data)

    assert 4 == len(signals)

    assert 28 == len(signal_graph)

    for s in signals:
        perf_content.add(URIRef("motivating_information"), s.identifier)

    perf_graph += signal_graph

    assert 33 == len(perf_graph)


def test_multiple_gap_values(perf_data):
    signal = Comparison()

    signals = signal.detect(perf_data)

    assert 4 == len(signals)

    expected_gap_sizes = [5.0, 1.0, -1.0, -10.0]

    for index, signal in enumerate(signals):
        v = signal.value(SLOWMO.PerformanceGapSize).value
        assert pytest.approx(v) == expected_gap_sizes[index]


def test_comparator_node(perf_data):
    signal = Comparison()

    signals = signal.detect(perf_data)

    expected_comparator_values = [85.0, 89.0, 91.0, 100.0]
    
    for index, signal in enumerate(signals):
        assert Literal(expected_comparator_values[index]) == signal.value(SLOWMO.RegardingComparator / RDF.value)
        

def test_empty_performance_content_returns_value_error():
    mi = Comparison()
    with pytest.raises(ValueError): 
        mi.detect(pd.DataFrame([[]]))

    
         


    

    