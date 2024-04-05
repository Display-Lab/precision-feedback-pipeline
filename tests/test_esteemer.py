import pandas as pd
import pytest
from rdflib import BNode, Graph, Literal, URIRef

from bitstomach.signals import Comparison, Trend
from esteemer import esteemer
from utils.namespace import PSDO, SLOWMO

TEMPLATE_A = "https://repo.metadatacenter.org/template-instances/9e71ec9e-26f3-442a-8278-569bcd58e708"


@pytest.fixture
def history():
    return {
        "2023-06-01": {
            "message_template": TEMPLATE_A,
            "acceptable_by": "Social better",
        },
        "2023-07-01": {
            "message_template": "different template B",
            "acceptable_by": "Social worse",
        },
        "2023-08-01": {
            "message_template": TEMPLATE_A,
            "acceptable_by": "Social better",
        },
        "2023-09-01": {
            "message_template": "different template A",
            "acceptable_by": "Social better",
        },
    }


@pytest.fixture
def performance_data_frame():
    performance_data = [
        [
            "staff_number",
            "measure",
            "month",
            "passed_rate",
            "passed_count",
            "flagged_count",
            "denominator",
            "peer_average_comparator",
            "peer_75th_percentile_benchmark",
            "peer_90th_percentile_benchmark",
            "goal_comparator_content",
        ],
        [157, "PONV05", "2022-08-01", 0.95, 85.0, 0, 100.0, 84.0, 88.0, 90.0, 99.0],
    ]
    return pd.DataFrame(performance_data[1:], columns=performance_data[0])


@pytest.fixture
def candidate_resource(performance_data_frame):
    graph = Graph()
    candidate_resource = graph.resource(BNode())
    candidate_resource[SLOWMO.RegardingComparator] = PSDO.peer_90th_percentile_benchmark
    candidate_resource[SLOWMO.AcceptableBy] = Literal("social better")
    candidate_resource[SLOWMO.AncestorTemplate] = URIRef(TEMPLATE_A)
    candidate_resource[SLOWMO.RegardingMeasure] = BNode("PONV05")

    motivating_informations = Comparison.detect(performance_data_frame)

    performance_content = graph.resource(BNode("performance_content"))
    for s in motivating_informations:
        s[SLOWMO.RegardingMeasure] = BNode("PONV05")
        performance_content.add(PSDO.motivating_information, s.identifier)
        graph += s.graph

    return candidate_resource


def test_score(candidate_resource):
    esteemer.score(candidate_resource, None, {})
    assert candidate_resource.value(SLOWMO.Score).value == pytest.approx(0.035)


def test_calculate_preference_score(candidate_resource):
    assert esteemer.calculate_preference_score(candidate_resource, {}) == 0


def test_select_candidate():
    graph = Graph()
    candidate1 = graph.resource(BNode("candidate1"))
    candidate2 = graph.resource(BNode("candidate2"))

    candidate1[SLOWMO.Score] = Literal(0.2)
    candidate2[SLOWMO.Score] = Literal(0.1)

    candidate1[SLOWMO.AcceptableBy] = Literal("social worse")
    candidate1[SLOWMO.AcceptableBy] = Literal("improving")

    # get graph that has candidates scored by esteemer
    selected_candidate = esteemer.select_candidate(graph)
    assert str(selected_candidate) in ["candidate1", "candidate2"]
    assert str(selected_candidate) == "candidate1"

    candidate3 = graph.resource(BNode("candidate3"))
    candidate3[SLOWMO.Score] = Literal(0.2)
    candidate3[SLOWMO.AcceptableBy] = Literal("social worse")
    selected_candidate = esteemer.select_candidate(graph)
    assert str(selected_candidate) in ["candidate1", "candidate3"]
    assert graph.resource(selected_candidate).value(SLOWMO.Score) == Literal(0.2)


def test_calculate_gap_motivating_info(candidate_resource):
    score_info = esteemer.calculate_motivating_info_score(candidate_resource)
    assert score_info["score"] == pytest.approx(0.035)
    assert PSDO.positive_performance_gap_content in score_info["type"]
    assert "number_of_months" not in score_info


def test_get_trend_info():
    candidate_resource = Trend._resource(0.0034)
    mods = Trend.moderators([candidate_resource])[0]
    assert mods["trend_size"] == pytest.approx(0.0034)
    assert Trend.signal_type in mods["type"]


# History scoring tests


def test_no_history_signal_is_score_0(candidate_resource):
    assert esteemer.calculate_history_score(candidate_resource, {}) == {"score": 0.0}

    assert esteemer.calculate_history_score(candidate_resource, None) == {"score": 0.0}


def test_history_with_two_recurrances(candidate_resource, history):
    info = esteemer.calculate_history_score(candidate_resource, history)

    assert info["score"] == round(2 / 11, 4) * -0.1
