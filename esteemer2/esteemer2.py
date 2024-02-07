import json
import random
from typing import List
from rdflib import RDF, BNode, Graph, Literal, URIRef


def score(performer_graph: Graph, candidate: BNode, history: json, preferences: json):
    """
    calculates score.

    Parameters:
    - performer_graph (Graph): the performer_graph.
    - candidate (BNode): The candidate message.
    - history (json): The message history.
    - preferences (json): The performer preferences.

    Returns:
    float: score.
    """
    # calculate sub-score
    # 1. based on motivating info
    motivating_info_score = calculate_motivating_info_score(performer_graph, candidate)

    # 2. based on history
    history_score = calculate_history_score(performer_graph, candidate, history)

    # 3. based on preferences
    preference_score = calculate_preference_score(
        performer_graph, candidate, preferences
    )

    # calculate final score = function of sub-scores
    final_score = motivating_info_score + history_score + preference_score

    # update the candidate with the score
    update_candidate_score(performer_graph, candidate, final_score)


def calculate_motivating_info_score(performer_graph: Graph, candidate: BNode) -> float:
    """
    calculates motivating info sub-score.

    Parameters:
    - performer_graph (Graph): the performer_graph.
    - candidate (BNode): The candidate message.

    Returns:
    float: motivating info sub score.
    """
    return 42


def calculate_history_score(
    performer_graph: Graph, candidate: BNode, history: json
) -> float:
    """
    calculates history sub-score.

    Parameters:
    - performer_graph (Graph): the performer_graph.
    - candidate (BNode): The candidate message.

    Returns:
    float: history sub-score.
    """
    return 43


def calculate_preference_score(
    performer_graph: Graph, candidate: BNode, preferences: json
) -> float:
    """
    calculates preference sub-score.

    Parameters:
    - performer_graph (Graph): the performer_graph.
    - candidate (BNode): The candidate message.
    - preferences (json): The performer preferences.

    Returns:
    float: preference sub-score.
    """
    return 44


def update_candidate_score(performer_graph: Graph, candidate: BNode, score: float):
    """
    updates candidate score

    Parameters:
    - performer_graph (Graph): The graph to add the score to.
    - candidate (BNode): The candidate message.
    - score (float): The score.

    Returns:
    """
    performer_graph.add(
        (candidate, URIRef("http://example.com/slowmo#Score"), Literal(str(score)))
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
    max_score = max([score for _, score in performer_graph.subject_objects(URIRef("http://example.com/slowmo#Score"))], default=None)

    candidates_with_max_score = [(candidate) for candidate, score in performer_graph.subject_objects(URIRef("http://example.com/slowmo#Score"))
                        if score == max_score]
    
    # Randomly select one of the candidates with the known maximum score
    selected_candidate = random.choice(candidates_with_max_score)

    performer_graph.add((selected_candidate, URIRef("slowmo:selected"), Literal(True)))

    return selected_candidate
