from typing import List, Optional, Tuple
from rdflib import RDF, BNode, Graph, URIRef
from rdflib.resource import Resource
from utils.namespace import PSDO


class Comparison(Graph):

    def _detect(self, perf_info) -> Tuple[int, int]:
        return (3, 4)

    def detect(self, perf_content) -> Optional[List[Resource]]:
        
        self._detect(perf_content)
        
        r = self.resource(BNode("motivating_info"))

        r.add(RDF.type, PSDO.performance_gap_content)
        r.add(RDF.type, PSDO.positive_performance_gap_content)
        
        r2 = self.resource(BNode("motivating_info2"))

        r2.add(RDF.type, PSDO.performance_gap_content)
        r2.add(RDF.type, PSDO.positive_performance_gap_content)

        return [r,r2]
    
