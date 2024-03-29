import pytest
from rdflib import BNode, Graph, RDF, Literal, URIRef
from candidate_pudding import candidate_pudding
from rdflib.resource import Resource
from utils.namespace import SLOWMO, PSDO


@pytest.fixture
def graph():
    graph = Graph() 
    
    measure = graph.resource(BNode("PONV05"))
    measure[RDF.type] = URIRef("http://purl.obolibrary.org/obo/PSDO_0000102")
    
    template = graph.resource(URIRef("https://repo.metadatacenter.org/template-instances/9e71ec9e-26f3-442a-8278-569bcd58e708"))
    template[RDF.type] = URIRef("http://data.bioontology.org/ontologies/PSDO/classes/http://purl.obolibrary.org/obo/PSDO_0000002")
    template[URIRef("https://schema.metadatacenter.org/properties/26450fa6-bb2c-4126-8229-79efda7f863a")] = Literal("Opportunity to Improve Top 10 Peer Benchmark")
    template[URIRef("https://schema.metadatacenter.org/properties/6b9dfdf9-9c8a-4d85-8684-a24bee4b85a8")] = Literal(
        "You may have an opportunity to improve for the measure [measure name]. Your performance was [recipient performance level], below the top 10% peer benchmark, which was [comparator performance level] this month.")
    template.add(URIRef("http://purl.obolibrary.org/obo/IAO_0000136"),URIRef("http://purl.obolibrary.org/obo/PSDO_0000116"))
    template.add(URIRef("http://purl.obolibrary.org/obo/IAO_0000136"),PSDO.peer_90th_percentile_benchmark)
    
    comparator = graph.resource(PSDO.peer_90th_percentile_benchmark)
    comparator[RDF.type] = PSDO.comparator_content
    
    
    
    return graph

def test_create_candidate(graph):
    # given
    measure = graph.resource(BNode("PONV05"))
    template = graph.resource(URIRef("https://repo.metadatacenter.org/template-instances/9e71ec9e-26f3-442a-8278-569bcd58e708"))
    
    # when
    candidate = candidate_pudding.create_candidate(measure, template)
    
    # then
    assert candidate and isinstance(candidate, Resource) and isinstance(candidate.identifier, BNode)
    assert candidate.value(RDF.type).identifier == SLOWMO.Candidate
    assert candidate.value(SLOWMO.RegardingMeasure) == measure
    assert candidate.value(SLOWMO.AncestorTemplate) == template

def test_add_convenoience_properties(graph):
    # given
    measure = graph.resource(BNode("PONV05"))
    template = graph.resource(URIRef("https://repo.metadatacenter.org/template-instances/9e71ec9e-26f3-442a-8278-569bcd58e708"))
    candidate = candidate_pudding.create_candidate(measure, template)

    # when
    candidate = candidate_pudding.add_convenience_properties(candidate)
    
    assert candidate.value(SLOWMO.name) == Literal("Opportunity to Improve Top 10 Peer Benchmark")
    assert candidate.value(URIRef("psdo:PerformanceSummaryTextualEntity")) == Literal(
        "You may have an opportunity to improve for the measure [measure name]. Your performance was [recipient performance level], below the top 10% peer benchmark, which was [comparator performance level] this month.")
    assert candidate.value(SLOWMO.RegardingComparator).identifier == PSDO.peer_90th_percentile_benchmark
