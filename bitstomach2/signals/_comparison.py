from typing import List, Optional
from pandas import DataFrame

from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from utils.namespace import PSDO, SLOWMO


class Comparison(Graph):
    def detect(
        self, perf_content: DataFrame
    ) -> Optional[List[Resource]]:
        """
        Detects comparison signals against any supplied comparators using performance levels in performance content. The signal is calculated as a simple difference. It returns a list of resources representing each signal detected.

        Parameters:
        - perf_content (DataFrame): The performance content.

        Returns:
        - List[Resource]: The list of signal resources. 
        """
        if (
            perf_content.empty            
        ):
            raise (ValueError)

        level = perf_content["passed_percentage"][-1:].to_list()[0]
        
        resources = []
        comp_cols = [
            "peer_average_comparator",
            "peer_75th_percentile_benchmark",
            "peer_90th_percentile_benchmark",
            "goal_comparator_content"
        ]
        comparators = perf_content[-1:][comp_cols].to_dict(orient='records')[0]
        measure = BNode((perf_content["measure"].to_list()[0]))
        
        for key, value in comparators.items():
            gap = self._detect(level, value)

            # Add the signal node and value
            r = self.resource(BNode())
            r.add(RDF.type, PSDO.performance_gap_content)
            r.add(SLOWMO.PerformanceGapSize, Literal(gap))
            r.add(
                RDF.type,
                PSDO.positive_performance_gap_content
                if gap >= 0
                else PSDO.negative_performance_gap_content,
            )
            r.add(SLOWMO.RegardingMeasure, measure)
            

            # Add the comparator
            c = self.resource(BNode())
            c.set(RDF.type, PSDO[key])
            c.set(RDF.value, Literal(value))

            r.add(SLOWMO.RegardingComparator, c)

            resources.append(r)

        return resources

    def _detect(self, level, comparator) -> float:
        """Calculate gap (size, comparator) tuples from levels and comparators"""

        return (level - comparator)
