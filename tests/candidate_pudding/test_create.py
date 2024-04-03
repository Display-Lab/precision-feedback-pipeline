import pytest
from rdflib import BNode, Graph, RDF, Literal, URIRef, XSD
from candidate_pudding import candidate_pudding
from rdflib.resource import Resource
from utils.namespace import SLOWMO, PSDO
from bitstomach2.signals import Comparison

@pytest.fixture
def graph():
    graph = Graph() 
    
    measure = graph.resource(BNode("PONV05"))
    measure[RDF.type] = URIRef("http://purl.obolibrary.org/obo/PSDO_0000102")
    
    template = graph.resource(URIRef("https://repo.metadatacenter.org/template-instances/9e71ec9e-26f3-442a-8278-569bcd58e708"))
    template[RDF.type] = candidate_pudding.PERFORMANCE_SUMMARY_DISPLAY_TEMPLATE
    # template[URIRef("https://schema.metadatacenter.org/properties/26450fa6-bb2c-4126-8229-79efda7f863a")] = Literal("Opportunity to Improve Top 10 Peer Benchmark")
    template[URIRef("https://schema.metadatacenter.org/properties/6b9dfdf9-9c8a-4d85-8684-a24bee4b85a8")] = Literal(
        "You may have an opportunity to improve for the measure [measure name]. Your performance was [recipient performance level], below the top 10% peer benchmark, which was [comparator performance level] this month.")
    template.add(URIRef("http://purl.obolibrary.org/obo/IAO_0000136"),URIRef("http://purl.obolibrary.org/obo/PSDO_0000116"))
    template.add(URIRef("http://purl.obolibrary.org/obo/IAO_0000136"),PSDO.peer_90th_percentile_benchmark)
    template.add(URIRef("http://schema.org/name"), Literal("Opportunity to Improve Top 10 Peer Benchmark", datatype = XSD.string))
    
    comparator = graph.resource(PSDO.peer_90th_percentile_benchmark)
    comparator[RDF.type] = PSDO.comparator_content
    
    performance_content = graph.resource(BNode("performance_content"))
    performance_content.set(RDF.type, PSDO.performance_content)    
    signal = Comparison._resource(-0.04,"peer_90th_percentile_benchmark",0.94 )
    signal.add(SLOWMO.RegardingMeasure, measure)
    performance_content.add(URIRef("motivating_information"), signal)
    graph += signal.graph
    
    causal_pathway = graph.resource(URIRef("https://repo.metadatacenter.org/template-instances/f4006042-5750-4f6c-a039-fe0a88466464"))
    causal_pathway[URIRef("http://schema.org/name")] = Literal("social worse", datatype = XSD.string)
    
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
    
    assert candidate.value(SLOWMO.name) == Literal("Opportunity to Improve Top 10 Peer Benchmark", datatype = XSD.string)
    assert candidate.value(URIRef("psdo:PerformanceSummaryTextualEntity")) == Literal(
        "You may have an opportunity to improve for the measure [measure name]. Your performance was [recipient performance level], below the top 10% peer benchmark, which was [comparator performance level] this month.")
    assert candidate.value(SLOWMO.RegardingComparator).identifier == PSDO.peer_90th_percentile_benchmark

def test_add_motivating_information(graph):
    # given
    measure = graph.resource(BNode("PONV05"))
    template = graph.resource(URIRef("https://repo.metadatacenter.org/template-instances/9e71ec9e-26f3-442a-8278-569bcd58e708"))
    candidate = candidate_pudding.create_candidate(measure, template)    
   
    # when
    candidate = candidate_pudding.add_motivating_information(candidate)
    
    assert len(list(candidate[URIRef("motivating_information")]))>0 
    assert candidate.value(URIRef("motivating_information") / SLOWMO.RegardingMeasure) == measure