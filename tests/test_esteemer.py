from rdflib import BNode, URIRef
from esteemer2 import esteemer2
from tests.test_utils import get_graph


def test_score():
    graph = get_graph("tests/spek_tp.json")
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    esteemer2.score(graph, candidate, None, None)
    scores = graph.objects(
        subject=candidate, predicate=URIRef("http://example.com/slowmo#Score")
    )
    scores_list = list(scores)
    assert scores_list[0].value == "129"


def test_calculate_motivating_info_score():
    graph = get_graph("tests/spek_tp.json")
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")

    assert esteemer2.calculate_motivating_info_score(graph, candidate) == 42


def test_calculate_history_score():
    graph = get_graph("tests/spek_tp.json")
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")

    assert esteemer2.calculate_history_score(graph, candidate, None) == 43


def test_calculate_preference_score():
    graph = get_graph("tests/spek_tp.json")
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")

    assert esteemer2.calculate_preference_score(graph, candidate, None) == 44


def test_update_candidate_score():
    graph = get_graph("tests/spek_tp.json")
    candidate = BNode("N0fefdf2588e640068f19c40cd4dcb7ce")
    esteemer2.update_candidate_score(graph, candidate, 130)
    scores = graph.objects(
        subject=candidate, predicate=URIRef("http://example.com/slowmo#Score")
    )
    scores_list = list(scores)
    assert scores_list[0].value == "130"


def test_select_candidate():
    graph = get_graph(
        "tests/spek_st.json"
    )  # get graph that has candidates scored by esteemer
    selected_candidate = esteemer2.select_candidate(graph)
    assert str(selected_candidate) in [
        "N0fefdf2588e640068f19c40cd4dcb7ce",
        "N3840ed1cab81487f928030dbd6ac4489",

    ]
