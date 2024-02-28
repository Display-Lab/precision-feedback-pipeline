import pytest
from rdflib import BNode, Graph

from esteemer import utils


@pytest.fixture
def graph():
    graph = Graph().parse(source="tests/spek_tp.json", format="json-ld")

    global candidate_1
    global candidate_2
    global candidate_3
    global candidate_4
    candidate_1 = graph.resource(BNode("N3840ed1cab81487f928030dbd6ac4489"))
    candidate_2 = graph.resource(BNode("N0fefdf2588e640068f19c40cd4dcb7ce"))
    candidate_3 = graph.resource(BNode("N14f02942683f4712894a2c997baee53d"))
    candidate_4 = graph.resource(BNode("N53e6f7cfe6264b319099fc6080808331"))

    return graph


def test_measures(graph):
    measures = utils.measures(graph)
    blank_nodes = [BNode("PONV05"), BNode("SUS04"), BNode("TRAN04")]
    assert measures == blank_nodes


def test_candidates_returns_the_one_acceptable_for_measure(graph):
    measure_candidates = utils.candidates(
        graph, BNode("PONV05"), True
    )  # only one acceptable candidate

    assert len(measure_candidates) == 1

    assert candidate_1 in measure_candidates


def test_candidates_returns_all_acceptable(graph):
    acceptable_candidates = utils.candidates(graph, None, True)

    assert len(acceptable_candidates) == 2

    assert candidate_1 in acceptable_candidates
    assert candidate_2 in acceptable_candidates


def test_candidates_all(graph):
    candidates = utils.candidates(graph, None, False)

    assert len(candidates) == 4

    assert set([candidate_1, candidate_2, candidate_3, candidate_4]) == set(candidates)


def test_candidates_empty_or_no_match(graph):
    candidates = utils.candidates(graph, measure=BNode("nope"))

    assert len(candidates) == 0

    candidates = utils.candidates(Graph())

    assert len(candidates) == 0
