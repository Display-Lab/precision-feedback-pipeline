from typing import List, Optional

from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from utils.namespace import PSDO


class Comparison(Graph):
    def detect(self, perf_content: dict[str, List]) -> Optional[List[Resource]]:
        level = perf_content["levels"][-1]

        resources = []
        for comparator in perf_content["comparators"]:
            gap = self._detect(level, comparator)
            r = self.resource(BNode())
            r.add(RDF.type, PSDO.performance_gap_content)
            r.add(RDF.value, Literal(gap))

            # Add the comparator
            # c = self.resource(BNode())
            # c.set(RDF.type, PSDO[comparator.key])
            # c.set(RDF.value, comparator.value)

            # r.add(SLOWMO.RegardingComparator, c)

            resources.append(r)

        return resources

    def _detect(self, level, comparator) -> float:
        """Calculate gap (size, comparator) tuples from levels and comparators"""

        return level - comparator
