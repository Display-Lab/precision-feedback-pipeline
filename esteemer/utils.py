import random
from typing import List

from rdflib import DCTERMS, RDF, RDFS, BNode, Graph, URIRef
from rdflib.resource import Resource

from utils import PSDO, SLOWMO


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
) -> List[Resource]:
    """
    Retrieve a list of candidate resources from the performer graph.

    Parameters:
        performer_graph (Graph): The performer_graph.
        measure (BNode, optional): The measure to filter candidates. Defaults to None.
        filter_acceptable (bool, optional): Whether to filter candidates based on acceptability. Defaults to False.

    Returns:
        List[Resource]: A list of candidate BNodes.
    """

    candidates = [
        performer_graph.resource(subject)
        for subject in performer_graph.subjects(RDF.type, SLOWMO.Candidate)
    ]

    candidates = [
        candidate
        for candidate in candidates
        if (
            (
                measure is None
                or candidate.value(SLOWMO.RegardingMeasure).identifier == measure
            )
            and (
                not filter_acceptable
                or candidate.value(URIRef("slowmo:acceptable_by")) is not None
            )
        )
    ]

    return candidates


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

    # print(self.node)
    if candidate is None:
        s_m["message_text"] = "No message selected"
        return s_m
    else:
        temp_name = SLOWMO.name  # URI of template name?
        Display = ["text only", "bar chart", "line graph"]
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

        candidate_resource = performer_graph.resource(candidate)
        measure = candidate_resource.value(SLOWMO.RegardingMeasure)
        s_m["measure_name"] = str(measure.identifier)
        s_m["measure_title"] = measure.value(DCTERMS.title).value
        comparators = list(performer_graph.subjects(RDF.type, PSDO.comparator_content))

        for c_type in candidate_resource[SLOWMO.RegardingComparator / RDF.type]:
            if c_type.identifier in comparators:
                s_m["comparator_type"] = c_type.value(RDFS.label).value
                break

        return s_m


def candidates_records(performer_graph: Graph) -> List[List]:
    """
    provides the representation of candidates as a dictionary.

    Parameters:
    - performer_graph (Graph): The performer_graph.

    Returns:
    dict: The representation of candidates as a dictionary.
    """
    candidate_list = [
        [
            "staff_number",
            "measure",
            "month",
            "score",
            "motivating_score",
            "history_score",
            "name",
            "acceptable_by",
            "selected",
        ]
    ]

    for a_candidate in candidates(performer_graph):
        # representation = candidate_as_dictionary(a_candidate)
        representation = candidate_as_record(a_candidate)

        candidate_list.append(representation)
    return candidate_list


def candidate_as_record(a_candidate: Resource) -> List:
    representation = []

    representation.append(
        a_candidate.graph.value(
            BNode("p1"), URIRef("http://example.com/slowmo#IsAboutPerformer")
        ).value
    )
    representation.append(a_candidate.value(SLOWMO.RegardingMeasure).identifier)
    representation.append("N/A")
    score = a_candidate.value(SLOWMO.Score)
    representation.append(float(score.value) if score else None)
    representation.append(
        float(a_candidate.value(URIRef("motivating_score"))) if score else None
    )
    representation.append(
        float(a_candidate.value(URIRef("history_score"))) if score else None
    )
    representation.append(a_candidate.value(SLOWMO.name))
    representation.append(a_candidate.value(URIRef("slowmo:acceptable_by")))
    representation.append(a_candidate.value(URIRef("slowmo:selected")))

    return representation
