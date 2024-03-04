from typing import List

import pytest
from rdflib import RDF, BNode, Graph, URIRef
from rdflib.resource import Resource

from bitstomach2.signals import Comparison
from utils.namespace import PSDO


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
    comparison = mi.detect({"levels": [0.9], "comparators": [0.85, 0.89]})
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(mi, Graph)

    assert isinstance(comparison, List)
    assert isinstance(comparison[0], Resource)

    assert 2 == len(set(mi.subjects(RDF.type, PSDO.performance_gap_content)))


def test_node_is_aggregated_in_performance_info(perf_info):
    signal = Comparison()
    performance_info = perf_info.resource(BNode("performance_info"))

    # Create a small graph and return the base node(s) as a resource
    for s in signal.detect({"levels": [0.9], "comparators": [0.85, 0.89]}):
        performance_info.add(URIRef("motivating_information"), s.identifier)

    # Add the remaining triples (the whole subgraph) to teh perf graph
    perf_info += signal

    assert 7 == len(perf_info)

    assert 2 == len(set(perf_info.subjects(RDF.type, PSDO.performance_gap_content)))


def test_multiple_signals_from_single_detector(perf_info):
    performance_info = perf_info.resource(BNode("performance_info"))

    signal = Comparison()

    signals = signal.detect({"levels": [0.9], "comparators": [0.85, 0.89]})

    assert 2 == len(signals)

    assert 4 == len(signal)

    for s in signals:
        performance_info.add(URIRef("motivating_information"), s.identifier)

    perf_info += signal

    assert 7 == len(perf_info)


def test_multiple_gap_values():
    signal = Comparison()

    pc = {"levels": [0.7, 0.8, 0.9], "comparators": [0.85, 0.89, 0.91, 1.0]}

    signals = signal.detect(pc)

    assert 4 == len(signals)

    expected = [0.05, 0.01, -0.01, -0.1]

    for index, signal in enumerate(signals):
        v = signal.value(RDF.value).value
        assert pytest.approx(v) == expected[index]
