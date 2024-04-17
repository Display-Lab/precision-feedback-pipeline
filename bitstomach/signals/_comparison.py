from typing import List, Optional, Union

import pandas as pd
from rdflib import RDF, BNode, Literal, URIRef
from rdflib.resource import Resource

from bitstomach.signals import Signal
from utils.namespace import PSDO, SLOWMO


class Comparison(Signal):
    signal_type = PSDO.performance_gap_content

    @staticmethod
    def detect(perf_data: pd.DataFrame) -> Optional[List[Resource]]:
        """
        Detects comparison signals against a pre-defined list of comparators using performance levels in performance content.
        The signal is calculated as a simple difference. It returns a list of resources representing each signal detected.

        Parameters:
        - perf_content (DataFrame): The performance content.

        Returns:
        - List[Resource]: The list of signal resources.
        """

        if perf_data.empty:
            raise ValueError

        if not perf_data[-1:]["valid"].bool():
            return []

        resources = []

        gaps = Comparison._detect(perf_data)
        for key, value in gaps.items():
            r = Comparison._resource(value[0], key, value[1])
            resources.append(r)

        return resources

    @classmethod
    def _resource(
        cls, gap: float, comparator_name: str, comparator_value: float
    ) -> Resource:
        """
        adds the performance gap size, types it as positive or negative and adds the comparator to the subgraph
        """
        base = super()._resource()

        # Add the signal node and value
        base.add(SLOWMO.PerformanceGapSize, Literal(gap))
        base.add(
            RDF.type,
            PSDO.positive_performance_gap_content
            if gap >= 0
            else PSDO.negative_performance_gap_content,
        )

        # Add the comparator
        c = base.graph.resource(BNode())
        c.set(RDF.type, PSDO[comparator_name])
        c.set(RDF.value, Literal(comparator_value))

        base.add(SLOWMO.RegardingComparator, c)

        return base

    @staticmethod
    def _detect(perf_data: pd.DataFrame) -> dict:
        """Calculate gap from levels and comparators"""

        comp_cols = [
            "peer_average_comparator",
            "peer_75th_percentile_benchmark",
            "peer_90th_percentile_benchmark",
            "goal_comparator_content",
        ]

        gaps: dict = {}

        for comparator in comp_cols:
            comparator_value = perf_data[-1:][comparator] / 100

            gap = perf_data[-1:]["passed_rate"] - comparator_value
            gaps[comparator] = (float(gap), float(comparator_value))

        return gaps

    @classmethod
    def moderators(cls, motivating_informations: List[Resource]) -> List[dict]:
        """
        extracts comparison moderators (gap_size and comparator_type) from a suplied list of motivating information
        """
        mods = []

        for signal in super().select(motivating_informations):
            motivating_info_dict = super().moderators(signal)
            motivating_info_dict["gap_size"] = round(
                abs(signal.value(SLOWMO.PerformanceGapSize).value), 4
            )
            motivating_info_dict["comparator_type"] = signal.value(
                SLOWMO.RegardingComparator / RDF.type
            ).identifier

            mods.append(motivating_info_dict)

        return mods

    @classmethod
    def disposition(cls, mi: Resource) -> Union[List[Resource] | None]:
        if not super().select([mi]):
            return None

        disposition = super().disposition(mi)

        # extras
        comparator_type = mi.value(SLOWMO.RegardingComparator / RDF.type)

        disposition.append(comparator_type)

        disposition += list(comparator_type[RDF.type])
        TypeError
        return disposition

    @classmethod
    def exclude(cls, mi, message_roles: List[Resource]) -> bool:
        comparator_type = mi.value(SLOWMO.RegardingComparator / RDF.type)
        if comparator_type in message_roles:
            return False
        else:
            return True

    @staticmethod
    def comparator_type(mi: Resource) -> URIRef:
        return mi.value(SLOWMO.RegardingComparator / RDF.type).identifier
