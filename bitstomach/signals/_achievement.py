from typing import List, Optional

import pandas as pd
from rdflib import RDF, Literal, URIRef
from rdflib.resource import Resource

from bitstomach.signals import Comparison, Signal, Trend
from utils.namespace import PSDO, SLOWMO
import numpy as np

class Achievement(Signal):
    signal_type = PSDO.achievement_content

    @staticmethod
    def detect(perf_data: pd.DataFrame) -> Optional[List[Resource]]:
        if perf_data.empty:
            raise ValueError

        trend_signals = Trend.detect(perf_data)
        if (
            not trend_signals
            or not trend_signals[0][RDF.type : PSDO.positive_performance_trend_content]
        ):
            return []

        positive_comparison_signals = [
            s
            for s in Comparison.detect(perf_data)
            if s[RDF.type : PSDO.positive_performance_gap_content]
        ]

        negative_prior_month_comparisons = [
            s
            for s in Comparison.detect(perf_data.iloc[:-1], tiered_comparators=False)
            if s[RDF.type : PSDO.negative_performance_gap_content]
        ]

        achievement_signals = []

        for comparison_signal in positive_comparison_signals:
            previous_comparison_signal = next(
                (
                    comparison
                    for comparison in negative_prior_month_comparisons
                    if (
                        Comparison.comparator_type(comparison)
                        == Comparison.comparator_type(comparison_signal)
                    )
                ),
                None,
            )

            if not previous_comparison_signal:
                continue

            streak_length = Achievement._detect(perf_data,comparison_signal.value(SLOWMO.RegardingComparator))
            
            mi = Achievement._resource(
                trend_signals[0], comparison_signal, previous_comparison_signal, streak_length
            )

            achievement_signals.append(mi)
        return achievement_signals

    @classmethod
    def _resource(
        cls,
        trend_signal: Resource,
        comparison_signal: Resource,
        previous_comparison_signal: Resource,
        streak_length: int
    ) -> Resource:
        # create and type the Achievmente
        mi = super()._resource()
        mi.add(RDF.type, Comparison.signal_type)
        mi.add(RDF.type, Trend.signal_type)

        # set signal properties
        mi[SLOWMO.PerformanceTrendSlope] = trend_signal.value(
            SLOWMO.PerformanceTrendSlope
        )
        mi[SLOWMO.PerformanceGapSize] = comparison_signal.value(
            SLOWMO.PerformanceGapSize
        )
        mi[SLOWMO.PriorPerformanceGapSize] = previous_comparison_signal.value(
            SLOWMO.PerformanceGapSize
        )        
        mi[SLOWMO.StreakLength] = Literal(streak_length)

        # add comparator (Achievments are a Comparison)
        comparator = comparison_signal.value(SLOWMO.RegardingComparator)

        mi[SLOWMO.RegardingComparator] = comparator

        g = mi.graph
        g += comparison_signal.graph.triples((comparator.identifier, None, None))

        return mi

    @classmethod
    def disposition(cls, mi: Resource) -> List[Resource]:
        dispos = super().disposition(mi)
        dispos += Comparison.disposition(mi)
        dispos += Trend.disposition(mi)

        return dispos

    @classmethod
    def moderators(cls, motivating_informations: List[Resource]) -> List[dict]:
        """
        extracts achievement moderators (trend_slope, gap_size, comparator_type and prior_gap_size) from a suplied list of motivating information
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
            motivating_info_dict["trend_size"] = round(
                abs(signal.value(SLOWMO.PerformanceTrendSlope).value * 2), 4
            )
            motivating_info_dict["prior_gap_size"] = round(
                abs(signal.value(SLOWMO.PriorPerformanceGapSize).value), 4
            )
            motivating_info_dict["streak_length"] = signal.value(SLOWMO.StreakLength).value / 12

            mods.append(motivating_info_dict)

        return mods
    
    @staticmethod
    def _detect(perf_data: pd.DataFrame, comparator: Resource) -> float:
        """
        calculates the number of consecutive negative gaps prior to this months positive gap.
        """
        comp_cols = {
            PSDO["peer_average_comparator"]: "peer_average_comparator",
            PSDO["peer_75th_percentile_benchmark"]: "peer_75th_percentile_benchmark",
            PSDO["peer_90th_percentile_benchmark"]: "peer_90th_percentile_benchmark",
            PSDO["goal_comparator_content"]: "goal_comparator_content",
        }
        
        comparator_id = comparator.value(RDF.type).identifier

        gaps = perf_data["passed_rate"]-perf_data[comp_cols[comparator_id]]/100
        
        diff_reversed = gaps.values[:-1][::-1]
        first_positive_index = np.argmax(diff_reversed >= 0)
        count = np.sum(diff_reversed[:first_positive_index] < 0)
        count = count if count > 0 else len(diff_reversed)
        return count
