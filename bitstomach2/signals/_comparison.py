from typing import List, Optional

from pandas import DataFrame
from rdflib import RDF, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from utils.namespace import PSDO, SLOWMO


# TODO: Refactor to `class Comparison(Signal)` 
class Comparison(Graph):
    def detect(self, perf_content: DataFrame) -> Optional[List[Resource]]:
        """
        Detects comparison signals against any supplied comparators using performance levels in performance content. The signal is calculated as a simple difference. It returns a list of resources representing each signal detected.

        Parameters:
        - perf_content (DataFrame): The performance content.

        Returns:
        - List[Resource]: The list of signal resources.
        """
        if perf_content.empty:
            raise (ValueError)

        level = perf_content["passed_percentage"][-1:].to_list()[0]

        resources = []
        comp_cols = [
            "peer_average_comparator",
            "peer_75th_percentile_benchmark",
            "peer_90th_percentile_benchmark",
            "goal_comparator_content",
        ]
        comparators = perf_content[-1:][comp_cols].to_dict(orient="records")[0]
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

        return level - comparator

    @staticmethod
    def to_moderators(
        motivating_informations: List[Resource], comparator_type: URIRef
    ) -> dict:
        motivating_info_dict: dict = {}
        if not motivating_informations:
            return motivating_info_dict

        for motivating_information in motivating_informations:
            if PSDO.performance_gap_content not in [
                t.identifier for t in motivating_information.objects(RDF.type)
            ]:
                continue

            if (
                motivating_information.value(
                    SLOWMO.RegardingComparator / RDF.type
                ).identifier
                == comparator_type
            ):
                motivating_info = motivating_information

        motivating_info_dict["gap_size"] = motivating_info.value(
            SLOWMO.PerformanceGapSize
        ).value

        for gap_type in list(motivating_info[RDF.type]):
            if gap_type.identifier in (
                PSDO.positive_performance_gap_content,
                PSDO.negative_performance_gap_content,
            ):
                motivating_info_dict["type"] = gap_type

        return motivating_info_dict
