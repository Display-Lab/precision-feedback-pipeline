from rdflib import Namespace, URIRef

from utils.namespace import AliasingDefinedNamespace


class PSDO(AliasingDefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/")

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    PSDO_0000104: URIRef
    positive_performance_gap_content: URIRef

    PSDO_0000105: URIRef
    negative_performance_gap_content: URIRef

    PSDO_0000099: URIRef
    positive_performance_trend_content: URIRef
    
    PSDO_0000100: URIRef
    negative_performance_trend_content: URIRef

    _alias = {
        "positive_performance_gap_content": "PSDO_0000104",
        "negative_performance_gap_content": "PSDO_0000105",
        "positive_performance_trend_content": "PSDO_0000099",
        "negative_performance_trend_content": "PSDO_0000100"
    }
