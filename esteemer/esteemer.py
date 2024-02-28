import json
import random

from rdflib import RDF, XSD, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from utils.namespace import PSDO, RO, SLOWMO


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
        candidate_resource, final_score, motivating_info["number_of_months"]
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

    # our scoring function right now takes the absolute value of moderator for each causal pathway
    match causal_pathway.value:
        case "Social Worse":
            gap_size, type, number_of_months = get_gap_info(candidate_resource)
            score = round(abs(gap_size), 4) / 5 - 0.02
        case "Social better":
            gap_size, type, number_of_months = get_gap_info(candidate_resource)
            score = round(abs(gap_size), 4) + 0.02
        case "Improving":
            trend_size, type, number_of_months = get_trend_info(candidate_resource)
            score = round(abs(trend_size), 4) * 5
        case "Worsening":
            trend_size, type, number_of_months = get_trend_info(candidate_resource)
            score = round(abs(trend_size), 4)
        case _:
            score = 0.0
    return {"score": score, "type": type.n3(), "number_of_months": number_of_months}


def calculate_history_score(candidate_resource: Resource, history: json) -> float:
    """
    calculates history sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (json): The history of messages.

    Returns:
    float: history sub-score.
    """
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


def get_gap_info(candidate_resource: Resource) -> tuple[float, URIRef, None]:
    """
    returns gap size, gap type.

    Parameters:
    - candidate_resource (Resource): The candidate resource.


    Returns:
    tuple[float, URIRef, None]: [gap size, gap type, None]
    """
    performer_graph = candidate_resource.graph
    measure = candidate_resource.value(SLOWMO.RegardingMeasure)
    comparator = candidate_resource.value(SLOWMO.RegardingComparator)
    p1 = performer_graph.resource(BNode("p1"))

    dispositions: list[Resource] = [
        disposition
        for disposition in p1[RO.has_disposition]
        if (
            (
                disposition.identifier,
                SLOWMO.RegardingComparator,
                comparator.identifier,
            )
            in performer_graph
            and (
                disposition.identifier,
                SLOWMO.RegardingMeasure,
                measure.identifier,
            )
            in performer_graph
            and (
                (
                    disposition.identifier,
                    RDF.type,
                    PSDO.positive_performance_gap_content,
                )
                in performer_graph
                or (
                    disposition.identifier,
                    RDF.type,
                    PSDO.negative_performance_gap_content,
                )
                in performer_graph
            )
        )
    ]

    if len(dispositions) == 0:
        return 0, None

    gap_size = performer_graph.value(
        dispositions[0].identifier, SLOWMO.PerformanceGapSize, None
    ).value

    gap_type = performer_graph.value(
        dispositions[0].identifier, RDF.type, None
    )  # use gap_type.n3() to see the value
    return gap_size, gap_type, None


def get_trend_info(candidate_resource: Resource) -> tuple[float, URIRef, int]:
    """
    returns trend size, trend type and number of month.

    Parameters:
    - candidate_resource (Resource): The candidate resource.


    Returns:
    tuple[float, URIRef, None]: [trend size, trend type, number of month]
    """
    performer_graph: Graph = candidate_resource.graph
    measure = candidate_resource.value(SLOWMO.RegardingMeasure)

    p1 = performer_graph.resource(BNode("p1"))

    dispositions: list[Resource] = [
        disposition
        for disposition in p1[RO.has_disposition]
        if (
            (
                disposition.identifier,
                SLOWMO.RegardingMeasure,
                measure.identifier,
            )
            in performer_graph
            and (
                (
                    disposition.identifier,
                    RDF.type,
                    PSDO.positive_performance_trend_content,
                )
                in performer_graph
                or (
                    disposition.identifier,
                    RDF.type,
                    PSDO.negative_performance_trend_content,
                )
                in performer_graph
            )
        )
    ]

    if len(dispositions) == 0:
        return 0, None

    trend_size = performer_graph.value(
        dispositions[0].identifier,
        SLOWMO.PerformanceTrendSlope,
        None,
    ).value

    number_of_months = performer_graph.value(
        dispositions[0].identifier,
        SLOWMO.numberofmonths,
        None,
    ).value

    trend_type = performer_graph.value(dispositions[0].identifier, RDF.type, None)
    return float(trend_size), trend_type, number_of_months
