import random
from datetime import datetime
from typing import List

from rdflib import XSD, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from bitstomach.signals import Achievement, Approach, Comparison, Loss, Signal, Trend
from esteemer import utils
from esteemer.signals import History
from utils.namespace import PSDO, SLOWMO
from utils.settings import settings

MPM = {
    "social worse": {
        "comparison_size": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.5,
        "measure_recency": 0.5,
        "coachiness": 1.0,
    },
    "social better": {
        "comparison_size": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.9,
        "measure_recency": 0.5,
        "coachiness": 0.0,
    },
    "improving": {
        "trend_size": 0.8,
        "message_recency": 0.9,
        "message_received_count": 0.9,
        "measure_recency": 1.0,
        "coachiness": 0.5,
    },
    "worsening": {
        "trend_size": 0.8,
        "message_recency": 0.9,
        "message_received_count": 0.5,
        "measure_recency": 1.0,
        "coachiness": 1.0,
    },
    "goal gain": {
        "comparison_size": 0.5,
        "trend_size": 0.8,
        "achievement_recency": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.9,
        "measure_recency": 0.5,
        "coachiness": 0.5,
    },
    "goal loss": {
        "comparison_size": 0.5,
        "trend_size": 0.8,
        "loss_recency": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.5,
        "measure_recency": 0.5,
        "coachiness": 1.0,
    },
    "social gain": {
        "comparison_size": 0.5,
        "trend_size": 0.8,
        "achievement_recency": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.9,
        "measure_recency": 0.5,
        "coachiness": 0.5,
    },
    "social loss": {
        "comparison_size": 0.5,
        "trend_size": 0.8,
        "loss_recency": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.5,
        "measure_recency": 0.5,
        "coachiness": 1.0,
    },
    "goal worse": {
        "comparison_size": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.5,
        "measure_recency": 0.5,
        "coachiness": 1.0,
    },
    "social approach": {
        "comparison_size": 0.5,
        "trend_size": 0.8,
        "achievement_recency": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.9,
        "measure_recency": 1.0,
        "coachiness": 1.0,
    },
    "goal approach": {
        "comparison_size": 0.5,
        "trend_size": 0.8,
        "achievement_recency": 0.5,
        "message_recency": 0.9,
        "message_received_count": 0.9,
        "measure_recency": 1.0,
        "coachiness": 1.0,
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

    CAUSAL_PATHWAY = {
        "social better": {"score": score_better, "rules": rule_social_highest},
        "social worse": {"score": score_worse, "rules": null_rule},
        "improving": {"score": score_improving, "rules": null_rule},
        "worsening": {"score": score_worsening, "rules": null_rule},
        "goal gain": {"score": score_gain, "rules": null_rule},
        "goal loss": {"score": score_loss, "rules": null_rule},
        "social gain": {"score": score_gain, "rules": rule_social_highest},
        "social loss": {"score": score_loss, "rules": rule_social_lowest},
        "goal worse": {"score": score_worse, "rules": null_rule},
        "goal approach": {"score": score_approach, "rules": null_rule},
        "social approach": {"score": score_approach, "rules": rule_social_lowest},
    }

    causal_pathway = candidate.value(SLOWMO.AcceptableBy)
    motivating_informations = list(candidate[PSDO.motivating_information])
    rules = CAUSAL_PATHWAY[causal_pathway.value]["rules"]
    score_mi = CAUSAL_PATHWAY[causal_pathway.value]["score"]

    # rules

    if not rules(candidate):
        return None

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

    # coachiness
    coachiness_score = MPM[causal_pathway.value]["coachiness"]
    candidate[URIRef("coachiness_score")] = Literal(
        coachiness_score, datatype=XSD.double
    )

    final_calculated_score = final_score(mi_score, history_score, preference_score)

    candidate[SLOWMO.Score] = Literal(final_calculated_score, datatype=XSD.double)

    return candidate


def final_score(m, h, p):
    """
    the function, final_score,  takes two inputs, s and p. the range for s is 0 to 1. the range for p is -2 to +2.  The function f(s,p) increases with either s or p increasing. The function should have the following constraints: f(1,-2) == f(.5, 0) == f(0,2) and f(0.5, -2) == f(0.25, -1) == f(0, 0).
    """

    score = m * 1 + h * 2 + p * 1.3

    return round(score, 2)


def score_better(candidate: Resource, motivating_informations: List[Resource]) -> float:
    moderators = comparator_moderators(candidate, motivating_informations, Comparison)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = moderators["gap_size"]  # * mpm["comparison_size"]

    return score


def null_rule(candidate):
    return True


def rule_social_highest(candidate: Resource):
    # TODO: see if we can refactor to a better query
    causal_pathway = candidate.value(SLOWMO.AcceptableBy).value
    if candidate[SLOWMO.RegardingComparator : PSDO.peer_average_comparator]:
        candidates = utils.candidates(
            candidate.graph,
            candidate.value(SLOWMO.RegardingMeasure).identifier,
            filter_acceptable=True,
        )
        return not any(
            (
                candid[SLOWMO.RegardingComparator : PSDO.peer_90th_percentile_benchmark]
                or candid[
                    SLOWMO.RegardingComparator : PSDO.peer_75th_percentile_benchmark
                ]
            )
            and candid.value(SLOWMO.AcceptableBy).value == causal_pathway
            for candid in candidates
        )

    if candidate[SLOWMO.RegardingComparator : PSDO.peer_75th_percentile_benchmark]:
        candidates = utils.candidates(
            candidate.graph,
            candidate.value(SLOWMO.RegardingMeasure).identifier,
            filter_acceptable=True,
        )
        return not any(
            candid[SLOWMO.RegardingComparator : PSDO.peer_90th_percentile_benchmark]
            and candid.value(SLOWMO.AcceptableBy).value == causal_pathway
            for candid in candidates
        )

    return True


def rule_social_lowest(candidate: Resource):
    # TODO: see if we can refactor to a better query
    causal_pathway = candidate.value(SLOWMO.AcceptableBy).value
    if candidate[SLOWMO.RegardingComparator : PSDO.peer_90th_percentile_benchmark]:
        candidates = utils.candidates(
            candidate.graph,
            candidate.value(SLOWMO.RegardingMeasure).identifier,
            filter_acceptable=True,
        )
        return not any(
            (
                candid[SLOWMO.RegardingComparator : PSDO.peer_average_comparator]
                or candid[
                    SLOWMO.RegardingComparator : PSDO.peer_75th_percentile_benchmark
                ]
            )
            and candid.value(SLOWMO.AcceptableBy).value == causal_pathway
            for candid in candidates
        )

    if candidate[SLOWMO.RegardingComparator : PSDO.peer_75th_percentile_benchmark]:
        candidates = utils.candidates(
            candidate.graph,
            candidate.value(SLOWMO.RegardingMeasure).identifier,
            filter_acceptable=True,
        )
        return not any(
            candid[SLOWMO.RegardingComparator : PSDO.peer_average_comparator]
            and candid.value(SLOWMO.AcceptableBy).value == causal_pathway
            for candid in candidates
        )

    return True


def score_worse(candidate: Resource, motivating_informations: List[Resource]) -> float:
    moderators = comparator_moderators(candidate, motivating_informations, Comparison)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = moderators["gap_size"]  # * mpm["comparison_size"]

    return score


def score_improving(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = Trend.moderators(motivating_informations)[0]
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = moderators["trend_size"]  # * mpm["trend_size"]

    return score


def score_worsening(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    # TODO: what should the response be if the candidate is not acceptable by worsening
    moderators = Trend.moderators(motivating_informations)[0]
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = moderators["trend_size"]  # * mpm["trend_size"]

    return score


def score_approach(
    candidate: Resource, motivating_informations: List[Resource]
) -> float:
    moderators = comparator_moderators(candidate, motivating_informations, Approach)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (
        moderators["gap_size"] * mpm["comparison_size"]
        + moderators["trend_size"] * mpm["trend_size"]
        + moderators["streak_length"] * mpm["achievement_recency"]
    ) / (mpm["comparison_size"] + mpm["trend_size"] + mpm["achievement_recency"])

    return score


def score_gain(candidate: Resource, motivating_informations: List[Resource]) -> float:
    moderators = comparator_moderators(candidate, motivating_informations, Achievement)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (
        moderators["gap_size"] * mpm["comparison_size"]
        + moderators["trend_size"] * mpm["trend_size"]
        + moderators["streak_length"] * mpm["achievement_recency"]
    ) / (mpm["comparison_size"] + mpm["trend_size"] + mpm["achievement_recency"])

    return score


def score_loss(candidate: Resource, motivating_informations: List[Resource]) -> float:
    moderators = comparator_moderators(candidate, motivating_informations, Loss)
    mpm = MPM[candidate.value(SLOWMO.AcceptableBy).value]

    score = (
        moderators["gap_size"] * mpm["comparison_size"]
        + moderators["trend_size"] * mpm["trend_size"]
        + moderators["streak_length"] * mpm["loss_recency"]
    ) / (mpm["comparison_size"] + mpm["trend_size"] + mpm["loss_recency"])

    return score


def comparator_moderators(candidate, motivating_informations, signal: Signal):
    comparator_type = candidate.value(SLOWMO.RegardingComparator).identifier

    moderators = signal.moderators(motivating_informations)

    scoring_detail = [
        moderator
        for moderator in moderators
        if moderator["comparator_type"] == comparator_type
    ][0]

    return scoring_detail


def score_history(candidate: Resource, history) -> float:
    """
    calculates history sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - history (dict): The history of messages.

    Returns:
    float: history sub-score.
    """
    if not history or not settings.use_history:
        return 1.0

    # turn candidate resource into a 'history' element for the current month
    g: Graph = candidate.graph
    performance_month = next(g.objects(None, SLOWMO.PerformanceMonth)).value
    # add to history
    # history[performance_month] = History.to_element(candidate)

    signals = History.detect(
        history,
        {datetime.fromisoformat(performance_month): History.to_element(candidate)},
    )

    if not signals:
        return 1.0

    mod = History.moderators(signals)[0]

    causal_pathway = candidate.value(SLOWMO.AcceptableBy)

    return (
        mod["message_recurrence"] * MPM[causal_pathway.value]["message_received_count"]
        + mod["message_recency"] * MPM[causal_pathway.value]["message_recency"]
        + mod["measure_recency"] * MPM[causal_pathway.value]["measure_recency"]
    ) / (
        MPM[causal_pathway.value]["message_received_count"]
        + MPM[causal_pathway.value]["message_recency"]
        + MPM[causal_pathway.value]["measure_recency"]
    )


def score_preferences(candidate_resource: Resource, preferences: dict) -> float:
    """
    calculates preference sub-score.

    Parameters:
    - candidate_resource (Resource): The candidate resource.
    - preferences (json): The performer preferences.

    Returns:
    float: preference sub-score.
    """

    if not settings.use_preferences:
        return 0.0

    # map causal pathway schema:name to preferences key from the input
    map_cp_to_preferences = {
        "social better": "Social better",
        "social worse": "Social worse",
        "improving": "Improving",
        "worsening": "Worsening",
        "goal gain": "Goal gain",
        "goal loss": "Social loss",  # goal loss uses Social loss preferences value
        "social gain": "Social gain",
        "social loss": "Social loss",
        "goal worse": "Social worse",  # goal worse uses Social worse preferences value
        "social approach": "Social approach",
        "goal approach": "Goal approach",
    }

    key = map_cp_to_preferences.get(candidate_resource.value(SLOWMO.AcceptableBy).value)
    return preferences.get(key, 0.0)


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

    # filter acceptable candidates
    candidates = utils.candidates(performer_graph, filter_acceptable=True)

    # filter scored candidates
    candidates = [
        candidate
        for candidate in candidates
        if (candidate.value(URIRef("coachiness_score")) is not None)
    ]

    if settings.use_coachiness:
        # filter highest coachiness candidates
        highest_coachiness_candidates = candidates_from_coachiness_category(
            candidates, category=1.0
        )
        if not highest_coachiness_candidates:
            highest_coachiness_candidates = candidates_from_coachiness_category(
                candidates, category=0.5
            )
        if highest_coachiness_candidates:
            candidates = highest_coachiness_candidates

    max_score = max(
        [candidate.value(SLOWMO.Score).value for candidate in candidates],
        default=None,
    )

    candidates_with_max_score = [
        (candidate.identifier)
        for candidate in candidates
        if candidate.value(SLOWMO.Score).value == max_score
    ]

    # Randomly select one of the candidates with the known maximum score
    selected_candidate = random.choice(candidates_with_max_score)

    performer_graph.add((selected_candidate, SLOWMO.Selected, Literal(True)))

    return selected_candidate


def candidates_from_coachiness_category(candidates, category):
    return [
        candidate
        for candidate in candidates
        if (candidate.value(URIRef("coachiness_score")).value == category)
    ]
