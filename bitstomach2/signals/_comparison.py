from typing import List, Optional

from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from utils.namespace import PSDO, SLOWMO


class Comparison(Graph):
    def detect(
        self, perf_content: dict[str, dict[str, float]]
    ) -> Optional[List[Resource]]:
        """
        Detects comparison signals against any supplied comparators using performance levels in performance content. The signal is calculated as a simple difference. It returns a list of resources representing each signal detected.

        Parameters:
        - perf_content (dict[str, dict[str, float]]): The performance content.

        Returns:
        - List[Resource]: The list of signal resources. 
        """
        if (
            not perf_content
            or "levels" not in perf_content
            or "comparators" not in perf_content
        ):
            raise (ValueError)

        level = perf_content["levels"][-1]

        resources = []
        for key, value in perf_content["comparators"].items():
            gap = self._detect(level, value)

            # Add the signal node and value
            r = self.resource(BNode())
            r.add(RDF.type, PSDO.performance_gap_content)
            r.add(RDF.value, Literal(gap))
            r.add(
                RDF.type,
                PSDO.positive_performance_gap_content
                if gap >= 0
                else PSDO.negative_performance_gap_content,
            )

            # Add the comparator
            c = self.resource(BNode())
            c.set(RDF.type, PSDO[key])
            c.set(RDF.value, Literal(value))

            r.add(SLOWMO.RegardingComparator, c)

            resources.append(r)

        return resources

    def _detect(self, level, comparator) -> float:
        """Calculate gap (size, comparator) tuples from levels and comparators"""

        return level - comparator
