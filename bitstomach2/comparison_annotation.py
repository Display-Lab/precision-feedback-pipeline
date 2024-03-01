from typing import Optional
from rdflib import RDF, BNode, Graph, URIRef
from rdflib.resource import Resource


class Comparison:
    def annotate(self, perf_content) -> Optional[Resource]:
        # TODO document why this method is empty

        r = Graph().resource(BNode("annotation1"))

        r.set(RDF.type, URIRef("comparison"))

        return r
