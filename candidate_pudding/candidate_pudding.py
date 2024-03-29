from rdflib import BNode, RDF, Literal, URIRef
from rdflib.resource import Resource
from utils.namespace import SLOWMO, PSDO

def create_candidate(measure: Resource, template: Resource):
    candidate = measure.graph.resource(BNode())
    candidate[RDF.type] = SLOWMO.Candidate
    candidate[SLOWMO.RegardingMeasure] = measure
    candidate[SLOWMO.AncestorTemplate] = template
    
    # TODO: add in motivating information link
    return candidate

def acceptable_by(candidate: Resource):
    candidate[URIRef("slowmo:acceptable_by")] = Literal("Improving")
    return candidate

def get_messages_with_causal_pathways():
    # returns all the messages out of the base graph and include the causal pathway that their candidates could be accpeted by. This causal pathway could 
    # be added at startup to the templates
    return 

def add_convenience_properties(candidate: Resource):
    candidate[SLOWMO.name] = candidate.value(
        SLOWMO.AncestorTemplate / 
        URIRef("https://schema.metadatacenter.org/properties/26450fa6-bb2c-4126-8229-79efda7f863a")
        )
    
    candidate[URIRef("psdo:PerformanceSummaryTextualEntity")] = candidate.value(
        SLOWMO.AncestorTemplate / 
        URIRef("https://schema.metadatacenter.org/properties/6b9dfdf9-9c8a-4d85-8684-a24bee4b85a8")
        )
    
    comparator = next((ttype for ttype in
        candidate[SLOWMO.AncestorTemplate / URIRef("http://purl.obolibrary.org/obo/IAO_0000136")]
        if ttype[RDF.type: PSDO.comparator_content]
        ), None)
    
    candidate[SLOWMO.RegardingComparator] = comparator or Literal(None) 
    return candidate
