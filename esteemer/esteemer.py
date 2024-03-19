import json
import random

from rdflib import RDF, XSD, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from bitstomach2.signals import Comparison, Trend
from utils.namespace import PSDO, RO, SLOWMO

from esteemer.signals import History


def score(candidate_resource: Resource, history: json, preferences: json):
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
    history_score = calculate_history_score(candidate_resource, history)

    # 3. based on preferences
    preference_score = calculate_preference_score(candidate_resource, preferences)

    # calculate final score = function of sub-scores
    final_score = motivating_info["score"] + history_score + preference_score

    # update the candidate with the score
    update_candidate_score(
        candidate_resource,
        final_score,
        motivating_info.setdefault("number_of_months", 0),
    )


def calculate_motivating_info_score(candidate_resource: Resource) -> dict:
    """
    calculates motivating info sub-score.

    Parameters:
    - performer_graph (Graph): the performer_graph.
    - candidate_resource (Resource): The candidate resource.

    Returns:
    dict: motivating info.
    """

    causal_pathway = list(candidate_resource.objects(URIRef("slowmo:acceptable_by")))[0]
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

            mod["score"] = round(abs(mod["gap_size"] / 100), 4) / 5 - 0.02
        case "Social better":
            comparator_type = candidate_resource.value(SLOWMO.IsAbout).identifier
            moderators = Comparison.moderators(motivating_informations)

            mod = [
                moderator
                for moderator in moderators
                if moderator["comparator_type"] == comparator_type
            ][0]

            mod["score"] = round(abs(mod["gap_size"] / 100), 4) + 0.02
        case "Improving":
            mod = Trend.moderators(motivating_informations)[0]
            mod["score"] = round(abs(mod["trend_size"] / 100), 4) * 5
        case "Worsening":
            mod = Trend.moderators(motivating_informations)[0]
            mod["score"] = round(abs(mod["trend_size"] / 100), 4)
        case _:
            mod["score"] = 0.0
    return mod


def calculate_history_score(candidate_resource: Resource, history: json) -> float:
    """
    calculates history sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (json): The history of messages.

    Returns:
    float: history sub-score.
    """
    # turn candidate resource into a 'history' element for the current month
    
    # add to history
    
    signals = History.detect(history)
    
    
    
    
    return 0


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


def update_candidate_score(
    candidate_resource: Resource, score: float, number_of_months: int
):
    """
    updates candidate score

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - score (float): The score.
    - number_of_months (int): The number of months.

    Returns:
    """
    performer_graph: Graph = candidate_resource.graph

    performer_graph.add(
        (
            candidate_resource.identifier,
            SLOWMO.Score,
            Literal(score, datatype=XSD.double),
        )
    )

    performer_graph.add(
        (
            candidate_resource.identifier,
            SLOWMO.numberofmonths,
            Literal(number_of_months),
        )
    )


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

