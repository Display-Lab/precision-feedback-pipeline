from typing import List, Optional

import pandas as pd
from rdflib import RDF, Literal
from rdflib.resource import Resource

from bitstomach2.signals import Signal
from utils import PSDO, SLOWMO


class Trend(Signal):
    # TODO: Allow an array of types
    signal_type = PSDO.performance_trend_content

    @staticmethod
    def detect(perf_data: pd.DataFrame) -> Optional[List[Resource]]:
        if perf_data.empty:
            raise ValueError

        if perf_data["passed_percentage"].count() < 3:
            return None

        slope = Trend._detect(perf_data)

        if not slope:
            return None

        return [Trend._resource(slope)]

    @classmethod
    def moderators(cls, motivating_informations: List[Resource]):
        mods = []

        for signal in super().select(motivating_informations):
            motivating_info_dict = super().moderators(signal)
            motivating_info_dict["trend_size"] = signal.value(
                SLOWMO.PerformanceTrendSlope
            ).value

            mods.append(motivating_info_dict)

        return mods.pop() if mods else {}

    @classmethod
    def _resource(cls, slope):
        base = super()._resource()

        if slope > 0:
            base.add(RDF.type, PSDO.positive_performance_trend_content)
        elif slope < 0:
            base.add(RDF.type, PSDO.negative_performance_trend_content)

        base[SLOWMO.PerformanceTrendSlope] = Literal(slope)

        return base

    @staticmethod
    def _detect(perf_data):
        performance_rates = perf_data["passed_percentage"]
        change_this_month = performance_rates.iloc[-1] - performance_rates.iloc[-2]
        change_last_month = performance_rates.iloc[-2] - performance_rates.iloc[-3]

        if change_this_month * change_last_month < 0:
            return 0

        return (performance_rates.iloc[-1] - performance_rates.iloc[-3]) / 2
