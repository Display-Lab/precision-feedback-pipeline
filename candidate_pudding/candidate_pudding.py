from rdflib import BNode, RDF, Graph, Literal, URIRef, XSD
from rdflib.resource import Resource
from utils.namespace import SLOWMO, PSDO, IAO

PERFORMANCE_SUMMARY_DISPLAY_TEMPLATE = URIRef("http://data.bioontology.org/ontologies/PSDO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPSDO_0000002")

def create_candidate(measure: Resource, template: Resource):
    
    candidate = measure.graph.resource(BNode())
    candidate[RDF.type] = SLOWMO.Candidate
    candidate[SLOWMO.RegardingMeasure] = measure
    candidate[SLOWMO.AncestorTemplate] = template
    
    add_convenience_properties(candidate)
    
    add_motivating_information(candidate)
    
    add_causal_pathway(candidate)
    
    return candidate

def add_motivating_information(candidate: Resource):
    performance_content = candidate.graph.resource(
        BNode("performance_content")
    )
    measure = candidate.value(SLOWMO.RegardingMeasure)
    motivating_informations = [
        motivating_info
        for motivating_info in performance_content[URIRef("motivating_information")]
        if motivating_info.value(SLOWMO.RegardingMeasure) == measure
    ]
    
    for motivating_information in motivating_informations:
        candidate.add(URIRef("motivating_information"), motivating_information )

    return candidate
    
def acceptable_by(candidate: Resource):
    CPO_has_preconditions = URIRef("http://purl.bioontology.org/ontology/SNOMEDCT/has_precondition")
    CP = candidate.value( SLOWMO.AncestorTemplate / SLOWMO.CausalPathway )  
    
    roles = list(candidate[ SLOWMO.AncestorTemplate / IAO.is_about ] )  
    mi_types = list(candidate[URIRef("motivating_information") / RDF.type])
    pre_conditions = set(CP[CPO_has_preconditions])
    
    dispositions = roles + mi_types
    
    if pre_conditions.issubset( dispositions):
        candidate[URIRef("slowmo:acceptable_by")] = CP.value(URIRef("http://schema.org/name"))
    # check if causal pathway pre-conditions match template roles and motivating information for the same measure
     
    return candidate

def add_causal_pathway(candidate: Resource):
    causal_pathway_map: dict = {
        "Congratulations High Performance": "social better",
        "Getting Worse": "worsening",
        "In Top 25%": "social better",
        "Opportunity to Improve Top 10 Peer Benchmark": "social worse",
        "Performance Improving": "improving"
    }
    AncestorTemplate = candidate.value(SLOWMO.AncestorTemplate)
    template_name = AncestorTemplate.value(URIRef("http://schema.org/name")).value
    causal_pathway_name = causal_pathway_map[template_name]
    causal_pathway_id = candidate.graph.value(None, URIRef("http://schema.org/name"), Literal(causal_pathway_name,datatype = XSD.string))
    candidate.value(SLOWMO.AncestorTemplate)[ SLOWMO.CausalPathway] = causal_pathway_id
    return candidate


def add_convenience_properties(candidate: Resource):
    candidate[SLOWMO.name] = candidate.value(
        SLOWMO.AncestorTemplate / 
        URIRef("http://schema.org/name")
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

def create_candidates(graph: Graph):
    for measure in graph[:RDF.type:PSDO.performance_measure_content]:
        measure_resource = graph.resource(measure)
        for template in graph[:RDF.type:PERFORMANCE_SUMMARY_DISPLAY_TEMPLATE]:
            template_resource = graph.resource(template)
            candidate = create_candidate(measure_resource, template_resource)            
            candidate = acceptable_by(candidate)
