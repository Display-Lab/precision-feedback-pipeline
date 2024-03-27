import json
import random

from rdflib import XSD, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from bitstomach2.signals import Comparison, Trend
from esteemer.signals import History
from utils.namespace import SLOWMO

MPM = {
    "Social Worse": {Comparison.signal_type: 0.5, History.signal_type: -0.5},
    "Social better": {Comparison.signal_type: 0.5, History.signal_type: -0.1},
    "Improving": {Trend.signal_type: 0.8, History.signal_type: -0.1},
    "Worsening": {Trend.signal_type: 0.8, History.signal_type: -0.5},
}


def score(candidate_resource: Resource, history: json, preferences: json) -> Resource:
    """
    calculates score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (json): The message history.
    - preferences (json): The performer preferences.

    Returns:
    float: score.
    """

    # calculate sub-score
    # 1. based on motivating info
    motivating_info = calculate_motivating_info_score(candidate_resource)

    # 2. based on history
    history_info = calculate_history_score(candidate_resource, history)

    # 3. based on preferences
    preference_score = calculate_preference_score(candidate_resource, preferences)

    # calculate final score = function of sub-scores
    final_score = motivating_info["score"] + history_info["score"] + preference_score

    candidate_resource[URIRef("motivating_score")] = Literal(
        motivating_info["score"], datatype=XSD.double
    )
    candidate_resource[URIRef("history_score")] = Literal(
        history_info["score"], datatype=XSD.double
    )

    candidate_resource[SLOWMO.Score] = Literal(final_score, datatype=XSD.double)

    return candidate_resource


def calculate_motivating_info_score(candidate_resource: Resource) -> dict:
    """
    calculates motivating info sub-score.

    Parameters:
    - performer_graph (Graph): the performer_graph.
    - candidate_resource (Resource): The candidate resource.

    Returns:
    dict: motivating info.
    """

    causal_pathway = candidate_resource.value(URIRef("slowmo:acceptable_by"))
    performance_content = candidate_resource.graph.resource(
        BNode("performance_content")
    )
    measure = candidate_resource.value(SLOWMO.RegardingMeasure)
    motivating_informations = [
        motivating_info
        for motivating_info in performance_content[URIRef("motivating_information")]
        if motivating_info.value(SLOWMO.RegardingMeasure) == measure
    ]

    mod = {}

    match causal_pathway.value:
        case "Social Worse":
            comparator_type = candidate_resource.value(SLOWMO.IsAbout).identifier

            moderators = Comparison.moderators(motivating_informations)

            mod = [
                moderator
                for moderator in moderators
                if moderator["comparator_type"] == comparator_type
            ][0]

            mod["score"] = (mod["gap_size"] / 5 - 0.02) * MPM[causal_pathway.value][
                Comparison.signal_type
            ]
        case "Social better":
            comparator_type = candidate_resource.value(SLOWMO.IsAbout).identifier
            moderators = Comparison.moderators(motivating_informations)

            mod = [
                moderator
                for moderator in moderators
                if moderator["comparator_type"] == comparator_type
            ][0]

            mod["score"] = (mod["gap_size"] + 0.02) * MPM[causal_pathway.value][
                Comparison.signal_type
            ]
        case "Improving":
            mod = Trend.moderators(motivating_informations)[0]
            mod["score"] = (mod["trend_size"] * 5) * MPM[causal_pathway.value][
                Trend.signal_type
            ]
        case "Worsening":
            mod = Trend.moderators(motivating_informations)[0]
            mod["score"] = (
                (mod["trend_size"]) * MPM[causal_pathway.value][Trend.signal_type]
            )
        case _:
            mod["score"] = 0.0
    return mod


def calculate_history_score(candidate_resource: Resource, history: dict) -> dict:
    """
    calculates history sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (dict): The history of messages.

    Returns:
    float: history sub-score.
    """
    if not history:
        return {"score": 0}

    # turn candidate resource into a 'history' element for the current month
    current_hist = History.to_element(candidate_resource)
    # add to history
    history.update(current_hist)

    signals = History.detect(history)

    if not signals:
        return {"score": 0}

    mod = History.moderators(signals)[0]

    causal_pathway = list(candidate_resource.objects(URIRef("slowmo:acceptable_by")))[0]

    mod["score"] = (
        mod["recurrence_count"] * MPM[causal_pathway.value][History.signal_type]
    )

    return mod


def calculate_preference_score(
    candidate_resource: Resource, preferences: json
) -> float:
    """
    calculates preference sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - preferences (json): The performer preferences.

    Returns:
    float: preference sub-score.
    """
    return 0


def select_candidate(performer_graph: Graph) -> BNode:
    """
    applies between measure business rules and selects the candidate based on scores.

    Parameters:
    - performer_graph (Graph): The performer_graph .

    Returns:
    BNode: selected candidate.
    """
    # 1. apply between measure business rules (future)

    # 2. select candidate

    # Find the max score
    max_score = max(
        [score for _, score in performer_graph.subject_objects(SLOWMO.Score)],
        default=None,
    )

    candidates_with_max_score = [
        (candidate)
        for candidate, score in performer_graph.subject_objects(SLOWMO.Score)
        if score == max_score
    ]

    # Randomly select one of the candidates with the known maximum score
    selected_candidate = random.choice(candidates_with_max_score)

    performer_graph.add((selected_candidate, URIRef("slowmo:selected"), Literal(True)))

    return selected_candidate
