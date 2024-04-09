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

        achievement_signals = []

        # call Comparison.detect(perf_data)
        # call Trend.detect(pref_data)
        # for each positive comparison signal
        #   if there is a negative gap for that comparator for previous month
        #       create an achievement and add
        #           everything from the comparison signal
        #           everything from the trend signal
        #           negative gap for the previous month
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
        # check if there is previsus month
        previous_gaps = Comparison._detect(perf_data.iloc[:-1])

        for signal in positive_comparison_signals:
            previous_gap = next(
                value[0]
                for key, value in previous_gaps.items()
                if PSDO[key]
                == signal.value(SLOWMO.RegardingComparator / RDF.type).identifier
            )

            if previous_gap >= 0:
                continue

            mi = Achievement._resource()
            mi[SLOWMO.PerformanceTrendSlope] = trend_signals[0].value(
                SLOWMO.PerformanceTrendSlope
            )
            mi[SLOWMO.PerformanceGapSize] = signal.value(SLOWMO.PerformanceGapSize)
            mi[SLOWMO.RegardingComparator] = signal.value(
                SLOWMO.RegardingComparator / RDF.type
            )
            achievement_signals.append(mi)
        return achievement_signals

    @classmethod
    def _resource(cls) -> Resource:
        mi = super()._resource()
        return mi
