import random
from typing import List

from rdflib import RDF, BNode, Graph, URIRef

from utils.namespace import PSDO, RO, SLOWMO


def measures(performer_graph: Graph) -> List[BNode]:
    """
    returns performer measures.

    Parameters:
    - performer_graph (Graph): The performer_graph.

    Returns:
    List[BNode]: returns list of performer measures.
    """
    measures = performer_graph.objects(
        URIRef("http://example.com/app#display-lab"),
        SLOWMO.IsAboutMeasure,
    )
    measure_list = list(measures)
    return measure_list


def candidates(
    performer_graph: Graph, measure: BNode = None, filter_acceptable: bool = False
) -> List[BNode]:
    """
    Retrieve a list of candidates from the performer graph.

    Parameters:
        performer_graph (Graph): The performer_graph.
        measure (BNode, optional): The measure to filter candidates. Defaults to None.
        filter_acceptable (bool, optional): Whether to filter candidates based on acceptability. Defaults to False.

    Returns:
        List[BNode]: A list of candidate BNodes.
    """
    candidates = [
        subject
        for subject in performer_graph.subjects(
            predicate=SLOWMO.RegardingMeasure,
            object=measure,
        )
        if (
            (subject, RDF.type, SLOWMO.Candidate) in performer_graph
            and (
                subject,
                URIRef("slowmo:acceptable_by") if filter_acceptable else None,
                None,
            )
            in performer_graph
        )
    ]

    return list(candidates)


# create an acceptable method
# use triples.triples
def measure_acceptable_candidates(
    performer_graph: Graph, measure: BNode
) -> List[BNode]:
    """
    extracts the list of acceptable candidates for a measure and applies measure business rules.

    Parameters:
    - performer_graph (Graph): The performer_graph.
    - measure (BNode): The measure.

    Returns:
    List[BNode]: returns list of acceptible candidates.
    """
    # extract the list of acceptible candidates for a measure
    candidate_list = candidates(
        performer_graph, filter_acceptable=True, measure=measure
    )

    # apply measure business rules
    candidate_list = apply_measure_business_rules(performer_graph, candidate_list)

    return candidate_list


def apply_measure_business_rules(
    performer_graph: Graph, candidate_list: List[BNode]
) -> List[BNode]:
    """
    applies measure business rules on candidate messages of a measure.

    Parameters:
    - performer_graph (Graph): The performer_graph.
    - candidate_list (List[BNode]): The candidate list.

    Returns:
    List[BNode]: returns the updated candidate list.
    """
    return candidate_list


def render(performer_graph: Graph, candidate: BNode) -> dict:
    """
    creates selected message from a selected candidate.

    Parameters:
    - performer_graph (Graph): The performer_graph.
    - candidate (BNode): The candidate.

    Returns:
    BNode: selected message.
    """
    s_m = {}
    a = 0
    # print(self.node)
    if candidate is None:
        s_m["message_text"] = "No message selected"
        return s_m
    else:
        temp_name = SLOWMO.name  # URI of template name?
        p232 = URIRef("psdo:PerformanceSummaryDisplay")
        Display = ["text only", "bar chart", "line graph"]
        comparator_types = ["Top 25", "Top 10", "Peers", "Goal"]
        sw = 0
        o2wea = []

        ## Format selected_candidate to return for pictoralist-ing
        for s21, p21, o21 in performer_graph.triples(
            (candidate, SLOWMO.AncestorTemplate, None)
        ):
            s_m["template_id"] = o21
        # Duplicate logic above and use to pull template name
        for s21, p21, o21 in performer_graph.triples((candidate, temp_name, None)):
            s_m["template_name"] = o21

        for s2, p2, o2 in performer_graph.triples(
            (candidate, URIRef("psdo:PerformanceSummaryTextualEntity"), None)
        ):
            s_m["message_text"] = o2
        # for s212,p212,o212 in self.spek_tp.triples((s,p232,None)):

        s_m["display"] = random.choice(Display)
        # for s9,p9,o9 in self.spek_tp.triples((s,p8,None)):
        #     s_m["Comparator Type"] = o9
        for s2we, p2we, o2we in performer_graph.triples(
            (candidate, URIRef("slowmo:acceptable_by"), None)
        ):
            o2wea.append(o2we)
        # print(*o2wea)
        s_m["acceptable_by"] = o2wea

        comparator_list = []

        for s5, p5, o5 in performer_graph.triples(
            (candidate, RO.has_disposition, None)
        ):
            s6 = o5
            # print(o5)
            for s7, p7, o7 in performer_graph.triples(
                (s6, SLOWMO.RegardingMeasure, None)
            ):
                s_m["measure_name"] = o7
                s10 = BNode(o7)
                for s11, p11, o11 in performer_graph.triples(
                    (s10, URIRef("http://purl.org/dc/terms/title"), None)
                ):
                    s_m["measure_title"] = o11
            for s14, p14, o14 in performer_graph.triples((s6, RDF.type, None)):
                # print(o14)
                if o14 == PSDO.peer_75th_percentile_benchmark:
                    comparator_list.append("Top 25")
                    # s_m["comparator_type"]="Top 25"
                if o14 == PSDO.peer_90th_percentile_benchmark:
                    comparator_list.append("Top 10")
                    # s_m["comparator_type"]="Top 10"
                if o14 == PSDO.peer_average_comparator:
                    comparator_list.append("Peers")
                    # s_m["comparator_type"]="Peers"
                if o14 == PSDO.goal_comparator_content:
                    comparator_list.append("Goal")
                    # s_m["comparator_type"]="Goal"
        for i in comparator_list:
            if i is not None:
                a = i
        s_m["comparator_type"] = a
        return s_m


def candidates_as_dictionary(performer_graph: Graph) -> dict:
    """
    provides the representation of candidates as a dictionary.

    Parameters:
    - performer_graph (Graph): The performer_graph.

    Returns:
    dict: The representation of candidates as a dictionary.
    """
    candidate_list = []

    for a_candidate in candidates(performer_graph):
        representation = candidate_as_dictionary(a_candidate, performer_graph)
        candidate_list.append(representation)
    return candidate_list


def candidate_as_dictionary(a_candidate: BNode, performer_graph: Graph) -> dict:
    representation = {}
    score = performer_graph.value(a_candidate, SLOWMO.Score, None)
    if score is not None:  # Literal('0.0') tests as false, so test for None explicitly
        score = round(
            float(score.value), 4
        )  # and we are explicit floating to eliminate numpy types that give the json decoder problems

    representation["score"] = score

    representation["number_of_months"] = performer_graph.value(
        a_candidate, SLOWMO.numberofmonths, None
    )

    representation["measure"] = performer_graph.value(
        a_candidate, SLOWMO.RegardingMeasure, None
    )
    representation["name"] = performer_graph.value(a_candidate, SLOWMO.name, None)
    representation["acceptable_by"] = list(
        performer_graph.objects(a_candidate, URIRef("slowmo:acceptable_by"))
    )  # converting to list ro allow repeated access
    representation["selected"] = performer_graph.value(
        a_candidate, URIRef("slowmo:selected"), None
    )

    return representation
