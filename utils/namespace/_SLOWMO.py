from rdflib import Namespace, URIRef

from utils.namespace import AliasingDefinedNamespace


class SLOWMO(AliasingDefinedNamespace):
    _NS = Namespace("http://example.com/slowmo#")
    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    RegardingMeasure: URIRef
    RegardingComparator: URIRef
    PerformanceGapSize2: URIRef
    PerformanceTrendSlope2: URIRef
    numberofmonths: URIRef
    Score: URIRef
    IsAboutMeasure: URIRef
    Candidate: URIRef
    name: URIRef
    AncestorTemplate: URIRef
