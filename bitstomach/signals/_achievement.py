from typing import List, Optional

import pandas as pd
from rdflib import RDF
from rdflib.resource import Resource

from bitstomach.signals import Comparison, Signal, Trend
from utils.namespace import PSDO, SLOWMO


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
            for s in Comparison.detect(perf_data.iloc[:-1])
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

            mi = Achievement._resource(
                trend_signals, comparison_signal, previous_comparison_signal
            )

            achievement_signals.append(mi)
        return achievement_signals

    @classmethod
    def _resource(
        cls, trend_signals, comparison_signal: Resource, previous_comparison_signal
    ) -> Resource:
        # create and type the Achievmente
        mi = super()._resource()
        mi.add(RDF.type, Comparison.signal_type)
        mi.add(RDF.type, Trend.signal_type)

        # set signal properties
        mi[SLOWMO.PerformanceTrendSlope] = trend_signals[0].value(
            SLOWMO.PerformanceTrendSlope
        )
        mi[SLOWMO.PerformanceGapSize] = comparison_signal.value(
            SLOWMO.PerformanceGapSize
        )
        mi[SLOWMO.PriorPerformanceGapSize] = previous_comparison_signal.value(
            SLOWMO.PerformanceGapSize
        )

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
