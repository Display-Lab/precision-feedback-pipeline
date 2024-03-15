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
    performance_data = [
        [
            "staff_number",
            "measure",
            "month",
            "passed_percentage",
            "passed_count",
            "flagged_count",
            "denominator",
            "peer_average_comparator",
            "peer_75th_percentile_benchmark",
            "peer_90th_percentile_benchmark",
            "goal_comparator_content",
        ],
        [157, "BP01", "2022-08-01", 85.0, 85.0, 0, 100.0, 84.0, 88.0, 90.0, 99.0],
        [157, "BP01", "2022-09-01", 90.0, 90.0, 0, 100.0, 85.0, 89.0, 91.0, 100.0],
    ]
    return pd.DataFrame(performance_data[1:], columns=performance_data[0])


def test_comp_annotation_creates_minimal_subgraph(perf_data):
    comparison = Comparison.detect(perf_data)
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(comparison, List)
    assert isinstance(comparison[0], Resource)
    assert 4 == len(comparison)
    assert 1 == len(
        set(comparison[0].graph.subjects(RDF.type, PSDO.performance_gap_content))
    )


def test_multiple_signals_from_single_detector(perf_info, perf_data):
    perf_graph, perf_content = perf_info

    signals = Comparison.detect(perf_data)

    assert 4 == len(signals)

    for s in signals:
        perf_content.add(URIRef("motivating_information"), s.identifier)
        perf_graph += s.graph

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
        assert Literal(expected_comparator_values[index]) == signal.value(
            SLOWMO.RegardingComparator / RDF.value
        )


def test_empty_performance_content_returns_value_error():
    mi = Comparison()
    with pytest.raises(ValueError):
        mi.detect(pd.DataFrame([[]]))


def test_moderators_return_dictionary():
    assert isinstance(Comparison.moderators([]), List)


def test_moderators_return_dictionary1():
    gap = 23
    graph = Graph()
    r = graph.resource(BNode())
    r.add(RDF.type, PSDO.performance_gap_content)
    r.add(SLOWMO.PerformanceGapSize, Literal(gap))
    r.add(
        RDF.type,
        PSDO.positive_performance_gap_content
        if gap >= 0
        else PSDO.negative_performance_gap_content,
    )
    r.add(SLOWMO.RegardingMeasure, BNode("PONV05"))

    # Add the comparator
    c = graph.resource(BNode())
    c.set(RDF.type, PSDO.peer_90th_percentile_benchmark)
    c.set(RDF.value, Literal(95.0))

    r.add(SLOWMO.RegardingComparator, c)

    moderators = Comparison.moderators([r])

    moderator = [
        moderator
        for moderator in moderators
        if moderator["comparator_type"] == PSDO.peer_90th_percentile_benchmark
    ][0]

    assert moderator["gap_size"] == 23
