from rdflib import BNode, Graph, URIRef
from esteemer2 import utils


def test_measures():
    measures = utils.measures(get_graph("tests/spek_tp.json"))
    blank_nodes = [BNode("PONV05"), BNode("SUS04"), BNode("TRAN04")]
    assert measures == blank_nodes


def test_measure_acceptable_candidates():
    graph = get_graph("tests/spek_tp.json")
    measure_acceptable_candidates = utils.measure_acceptable_candidates(
        graph, BNode("SUS04")
    )

    # Extract @id values for each BNode in the list
    id_values = []
    for bnode in measure_acceptable_candidates:
        # Query the graph for the @id value of the BNode
        id_value = str(bnode)
        if id_value:
            id_values.append(id_value)

    assert id_values == [
        "N0fefdf2588e640068f19c40cd4dcb7ce",
    ]


def test_measure_candidates():
    graph = get_graph("tests/spek_tp.json")
    measure_candidates = utils.measure_candidates(graph, BNode("PONV05"))

    # Extract @id values for each BNode in the list
    id_values = []
    for bnode in measure_candidates:
        # Query the graph for the @id value of the BNode
        id_value = str(bnode)
        if id_value:
            id_values.append(id_value)

    assert id_values == [
        "N3840ed1cab81487f928030dbd6ac4489",
    ]


def test_apply_measure_business_rules():
    graph = get_graph("tests/spek_tp.json")
    candidate_list = [
        BNode("N53e6f7cfe6264b319099fc6080808331"),
        BNode("N3840ed1cab81487f928030dbd6ac4489"),
    ]
    updated_candidate_list = utils.apply_measure_business_rules(graph, candidate_list)
    assert candidate_list == updated_candidate_list


def get_graph(file):
    # Specify the path to your JSON-LD file
    json_ld_file_path = file

    # Create an RDF graph using rdflib
    rdf_graph = Graph()

    # Parse JSON-LD data into the RDF graph
    graph = rdf_graph.parse(source=json_ld_file_path, format="json-ld")
    return graph
