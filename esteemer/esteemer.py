import random
from typing import List

from rdflib import XSD, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from bitstomach.signals import Achievement, Comparison, Loss, Signal, Trend
from esteemer.signals import History
from utils.namespace import PSDO, SLOWMO

MPM = {
    "social worse": {Comparison.signal_type: 0.5, History.signal_type: -0.5},
    "social better": {Comparison.signal_type: 0.5, History.signal_type: -0.1},
    "improving": {Trend.signal_type: 0.8, History.signal_type: -0.1},
    "worsening": {Trend.signal_type: 0.8, History.signal_type: -0.5},
    "goal gain": {
        Comparison.signal_type: 0.5,
        Trend.signal_type: 0.8,
        History.signal_type: -0.1,
    },
    "goal loss": {
        Comparison.signal_type: 0.5,
        Trend.signal_type: 0.8,
        History.signal_type: -0.5,
    },
}


def score(candidate: Resource, history: dict, preferences: dict) -> Resource:
    """
    calculates score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (json): The message history.
    - preferences (json): The performer preferences.

    Returns:
    float: score.
    """

    SCORING = {
        "social better": score_social_better,
        "social worse": score_social_worse,
        "improving": score_improving,
        "worsening": score_worsening,
        "goal gain": score_goal_gain,
        "goal loss": score_goal_loss,
    }

    causal_pathway = candidate.value(SLOWMO.AcceptableBy)
    motivating_informations = list(candidate[PSDO.motivating_information])
    score_mi = SCORING[causal_pathway.value]

    # MI
    mi_score = score_mi(candidate, motivating_informations)
    candidate[URIRef("motivating_score")] = Literal(mi_score, datatype=XSD.double)

    # History
    history_score = score_history(candidate, history)
    candidate[URIRef("history_score")] = Literal(history_score, datatype=XSD.double)

    # Preferences
    preference_score = score_preferences(candidate, preferences)
    candidate[URIRef("preference_score")] = Literal(
        preference_score, datatype=XSD.double
    )

    final_calculated_score = final_score((mi_score + history_score) , preference_score)

    candidate[SLOWMO.Score] = Literal(final_calculated_score, datatype=XSD.double)

    return candidate

def final_score(s, p):
    """
    the function, final_score,  takes two inputs, s and p. the range for s is 0 to 1. the range for p is -2 to +2.  The function f(s,p) increases with either s or p increasing. The function should have the following constraints: f(1,-2) == f(.5, 0) == f(0,2) and f(0.5, -2) == f(0.25, -1) == f(0, 0).
    """
    # Define the scaling factors for s and p
    scale_s = 4  # default to stated range of p
    scale_p = 1  # default to stated range of 2

    # Calculate the base value for the constraints, e.g. f(1,-2) == f(0.5, 0) == f(0,2)
    # base_value = scale_s * 0.5 + scale_p * 0.0  # default to mid-points of stated ranges
    base_value = scale_s * 0.5 + scale_p * 0  # default to mid-points of stated ranges

    # Adjust the function to increase with either s or p increasing
    return (scale_s * s + scale_p * p + base_value) / (scale_s + scale_p + base_value)

def score_social_better(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = social_moderators(candidate, motivating_informations)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (moderators["gap_size"] ) * mpm[Comparison.signal_type]

    return score


def score_social_worse(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = social_moderators(candidate, motivating_informations)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (moderators["gap_size"] ) * mpm[Comparison.signal_type]

    return score


def score_improving(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = Trend.moderators(motivating_informations)[0]
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (moderators["trend_size"] ) * mpm[Trend.signal_type]

    return score


def score_worsening(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    # TODO: what should the response be if the candidate is not acceptable by worsening
    moderators = Trend.moderators(motivating_informations)[0]
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (moderators["trend_size"]) * mpm[Trend.signal_type]

    return score


def score_goal_gain(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = achievement_and_loss_moderators(
        candidate, motivating_informations, Achievement
    )
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (
        moderators["gap_size"] * mpm[Comparison.signal_type]
        + moderators["trend_size"] * mpm[Trend.signal_type]
    )

    return score


def score_goal_loss(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = achievement_and_loss_moderators(
        candidate, motivating_informations, Loss
    )
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (
        moderators["gap_size"] * mpm[Comparison.signal_type]
        + moderators["trend_size"] * mpm[Trend.signal_type]
    ) 

    return score


def achievement_and_loss_moderators(candidate, motivating_informations, signal: Signal):
    comparator_type = candidate.value(SLOWMO.RegardingComparator).identifier

    moderators = signal.moderators(motivating_informations)

    scoring_detail = [
        moderator
        for moderator in moderators
        if moderator["comparator_type"] == comparator_type
    ][0]

    return scoring_detail


def social_moderators(candidate, motivating_informations):
    comparator_type = candidate.value(SLOWMO.RegardingComparator).identifier

    moderators = Comparison.moderators(motivating_informations)

    scoring_detail = [
        moderator
        for moderator in moderators
        if moderator["comparator_type"] == comparator_type
    ][0]

    return scoring_detail


def score_history(candidate, history) -> float:
    """
    calculates history sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (dict): The history of messages.

    Returns:
    float: history sub-score.
    """
    if not history:
        return 0

    # turn candidate resource into a 'history' element for the current month
    current_hist = History.to_element(candidate)
    # add to history
    history.update(current_hist)

    signals = History.detect(history)

    if not signals:
        return 0

    mod = History.moderators(signals)[0]
    score = mod["recurrence_count"]

    causal_pathway = candidate.value(SLOWMO.AcceptableBy)

    return score * MPM[causal_pathway.value][History.signal_type]


def score_preferences(candidate_resource: Resource, preferences: dict) -> float:
    """
    calculates preference sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - preferences (json): The performer preferences.

    Returns:
    float: preference sub-score.
    """

    # map causal pathway schema:name to preferences key from the input
    map_cp_to_preferences = {
        "social better": "Social better",
        "social worse": "Social worse",
        "improving": "Improving",
        "worsening": "Worsening",
        "goal gain": "Goal gain",
        "goal loss": "Social loss",  # goal loss uses Social loss preferences value
    }

    key = map_cp_to_preferences.get(candidate_resource.value(SLOWMO.AcceptableBy).value)
    return float(preferences.get(key, 0.0))


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
    if not set(performer_graph[: SLOWMO.AcceptableBy :]):
        return None

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

    performer_graph.add((selected_candidate, SLOWMO.Selected, Literal(True)))

    return selected_candidate
