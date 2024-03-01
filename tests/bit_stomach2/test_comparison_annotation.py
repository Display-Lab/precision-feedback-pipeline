import pytest
from rdflib import RDF, BNode, Graph, URIRef

from bitstomach2 import Comparison


@pytest.fixture
def perf_info() -> Graph:
    g = Graph()
    g.add(
        (BNode("PerformanceInformation"), RDF.type, URIRef("performance_information"))
    )
    assert 2 == len(g.all_nodes())
    return g


def test_comp_annotation_creates_minimal_subgraph():
    mi = Comparison()
    perf_data = {}
    a_node = BNode("annotation1")  # hard-coded for now

    resource = mi.annotate(perf_data)
    graph = resource.graph
    # logger.info(annotation_graph.serialize(format="json-ld"))

    assert isinstance(resource.graph, Graph)

    assert (a_node, None, None) in resource.graph
    assert graph[a_node]
    # either will assert that triples about 'annotation1' exist in the graph
    # Not sure how to directly test that a 'node' exists since a graph is a collection of triples

    assert URIRef("comparison") in set(graph[a_node : RDF.type])


def test_node_is_aggregation_in_performance_content(perf_info):
    mi = Comparison()
    perf_data = {}

    comparison = mi.annotate(perf_data)

    perf_info.add(
        (
            BNode("PerformanceInformation"),
            URIRef("motivating_information"),
            comparison.identifier,
        )
    )

    perf_info += comparison.graph

    assert 3 == len(perf_info)

    assert (comparison.identifier, RDF.type, URIRef("comparison")) in perf_info
