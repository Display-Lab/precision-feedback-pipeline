from typing import List, Optional

import pandas as pd
from rdflib import RDF
from rdflib.resource import Resource

from bitstomach.signals import Signal
from utils.namespace import PSDO, SLOWMO


class Achievement(Signal):
    signal_type = PSDO.achievement_content

    @staticmethod
    def detect(perf_data: pd.DataFrame) -> Optional[List[Resource]]:
        if perf_data.empty:
            raise ValueError

        # call Comparison.detect(perf_data)
        # call Trend.detect(pref_data)
        # for each positive comparison signal
        #   if there is a negative gap for that comparator for previous month
        #       create an achievement and add
        #           everything from the comparison signal
        #           everything from the trend signal
        #           negative gap for the previous month
        from bitstomach.signals import Comparison, Trend
        comparison_signals = Comparison.detect(perf_data)
        trend_signals = Trend.detect(perf_data)

        if not (comparison_signals and trend_signals):
            return None

        achievement_signals = []

        slope = trend_signals[0].value(SLOWMO.PerformanceTrendSlope).value

        for signal in comparison_signals:
            # continue on cases that are not achivement signals
            mi = Achievement._resource()
            mi[SLOWMO.PerformanceTrendSlope] = trend_signals[0].value(
                SLOWMO.PerformanceTrendSlope
            )
            mi[SLOWMO.PerformanceGapSize] = comparison_signals[0].value(
                SLOWMO.PerformanceGapSize
            )
            mi[SLOWMO.RegardingComparator] = comparison_signals[0].value(
                SLOWMO.RegardingComparator / RDF.type
            )
            achievement_signals.append(mi)
        return achievement_signals

    @classmethod
    def _resource(cls) -> Resource:
        mi = super()._resource()
        return mi
