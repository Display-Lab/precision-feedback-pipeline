import json
import random

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
    c = performer_graph.resource(candidate) #move this one as far as possibly you can
    causal_pathway = list(c.objects(URIRef("slowmo:acceptable_by")))[0]
    
    match  causal_pathway.value:
        case "Social Worse":
            gap_size, gap_type = get_gap_size_for_candidate(candidate, performer_graph)
            score = abs(gap_size)
        case "Social better":
            gap_size, gap_type = get_gap_size_for_candidate(candidate, performer_graph)
            score = gap_size
        case "Improving":
            score = 3
        case "Worsening":
            score = 4
        case _:
            score = 0
    return score
    #gap_size, gap_type = get_gap_size_for_candidate(candidate, performer_graph)
    #return gap_size
    # use case with an option per causal pathway

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
    return 0


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
    return 0


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
        (candidate, URIRef("http://example.com/slowmo#Score"), Literal(score))
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
        [
            score
            for _, score in performer_graph.subject_objects(
                URIRef("http://example.com/slowmo#Score")
            )
        ],
        default=None,
    )

    candidates_with_max_score = [
        (candidate)
        for candidate, score in performer_graph.subject_objects(
            URIRef("http://example.com/slowmo#Score")
        )
        if score == max_score
    ]

    # Randomly select one of the candidates with the known maximum score
    selected_candidate = random.choice(candidates_with_max_score)

    performer_graph.add((selected_candidate, URIRef("slowmo:selected"), Literal(True)))

    return selected_candidate


def get_gap_size_for_candidate(candidate: BNode, performer_graph: Graph):
    measure = performer_graph.value(
        candidate, URIRef("http://example.com/slowmo#RegardingMeasure"), None
    )

    comparator = performer_graph.value(
        candidate, URIRef("http://example.com/slowmo#RegardingComparator"), None
    )

    dispositions = [
        disposition
        for disposition in performer_graph.objects(
            subject=BNode("p1"),
            predicate=URIRef("http://purl.obolibrary.org/obo/RO_0000091"),
        )
        if (
            (
                disposition,
                URIRef("http://example.com/slowmo#RegardingComparator"),
                comparator,
            )
            in performer_graph
            and (
                disposition,
                URIRef("http://example.com/slowmo#RegardingMeasure"),
                measure,
            )
            in performer_graph
            and (
                (
                    disposition,
                    RDF.type,
                    URIRef("http://purl.obolibrary.org/obo/PSDO_0000104"),
                )
                in performer_graph
                or (
                    disposition,
                    RDF.type,
                    URIRef("http://purl.obolibrary.org/obo/PSDO_0000105"),
                )
                in performer_graph
            )
        )
    ]

    if len(dispositions) == 0:
        return 0, None

    gap_size = performer_graph.value(
        dispositions[0], URIRef("http://example.com/slowmo#PerformanceGapSize"), None
    ).value

    gap_type = performer_graph.value(
        dispositions[0], RDF.type, None
    )  # use gap_type.n3() to see the value
    return gap_size, gap_type
