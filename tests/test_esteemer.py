import pytest
from rdflib import BNode, Graph

from esteemer2 import esteemer2
from utils.namespace import SLOWMO


@pytest.fixture
def graph():
    return Graph().parse("tests/spek_tp.json")

def test_score(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)
    esteemer2.score(candidate_resource, None, None)
    scores = graph.objects(subject=candidate, predicate=SLOWMO.Score)
    scores_list = list(scores)
    assert scores_list[0].value == 0.0201


def test_calculate_motivating_info_score(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)

    assert (
        esteemer2.calculate_motivating_info_score(candidate_resource)["score"] == 0.0201
    )


def test_calculate_history_score(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)

    assert esteemer2.calculate_history_score(candidate_resource, None) == 0


def test_calculate_preference_score(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)

    assert esteemer2.calculate_preference_score(candidate_resource, None) == 0


def test_update_candidate_score(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)

    esteemer2.update_candidate_score(candidate_resource, 130, 3)
    scores = graph.objects(subject=candidate, predicate=SLOWMO.Score)
    scores_list = list(scores)
    assert scores_list[0].value == 130


def test_select_candidate():
    graph = Graph().parse("tests/spek_st.json")
    # get graph that has candidates scored by esteemer
    selected_candidate = esteemer2.select_candidate(graph)
    assert str(selected_candidate) in [
        "N0fefdf2588e640068f19c40cd4dcb7ce",
        "N3840ed1cab81487f928030dbd6ac4489",
    ]


def test_get_gap_info(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)
    gap_size, type, number_of_months = esteemer2.get_gap_info(candidate_resource)
    assert gap_size == 0.00009
    assert type.n3() == "<http://purl.obolibrary.org/obo/PSDO_0000104>"
    assert number_of_months is None


def test_get_trend_info(graph):
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    candidate_resource = graph.resource(candidate)
    trend_size, type, number_of_months = esteemer2.get_trend_info(candidate_resource)
    assert trend_size == 0.0034
    assert type.n3() == "<http://purl.obolibrary.org/obo/PSDO_0000099>"
    assert number_of_months == 1
