from typing import List, Optional

import pandas as pd
from rdflib import RDF, Literal
from rdflib.resource import Resource

from bitstomach.signals import Signal
from utils import PSDO, SLOWMO


class Trend(Signal):
    # TODO: Allow an array of types
    signal_type = PSDO.performance_trend_content

    @staticmethod
    def detect(perf_data: pd.DataFrame) -> Optional[List[Resource]]:
        """
        detects trend signals that are monotonic increasing or decreasing over three month. The trend slope is recorded as moderator.
        trend type is PSDO.performance_trend_content (positive or negative)
        """
        if perf_data.empty:
            raise ValueError

        slope = Trend._detect(perf_data)

        if not slope:
            return None

        return [Trend._resource(slope)]

    @classmethod
    def _resource(cls, slope: float) -> Resource:
        """
        adds the performance trend slope, types it as positive or negative to the subgraph

        """
        base = super()._resource()

        if slope > 0:
            base.add(RDF.type, PSDO.positive_performance_trend_content)
        elif slope < 0:
            base.add(RDF.type, PSDO.negative_performance_trend_content)

        base[SLOWMO.PerformanceTrendSlope] = Literal(slope)

        return base

    @classmethod
    def moderators(cls, motivating_informations: List[Resource]) -> List[dict]:
        """
        extract trend moderartor(trend_size) from a suplied list of motivating information
        """
        mods = []

        for signal in super().select(motivating_informations):
            motivating_info_dict = super().moderators(signal)
            motivating_info_dict["trend_size"] = round(
                abs(signal.value(SLOWMO.PerformanceTrendSlope).value), 4
            )

            mods.append(motivating_info_dict)

        return mods

    @staticmethod
    def _detect(perf_data: pd.DataFrame) -> float:
        """
        calcolates the slope of a monotonically increasing or decreasing trend over three month.
        """

        if perf_data["passed_rate"].count() < 3:
            return 0

        performance_rates = perf_data["passed_rate"]
        change_this_month = performance_rates.iloc[-1] - performance_rates.iloc[-2]
        change_last_month = performance_rates.iloc[-2] - performance_rates.iloc[-3]

        if change_this_month == 0:
            return 0

        if change_this_month * change_last_month < 0:
            return 0

        return (performance_rates.iloc[-1] - performance_rates.iloc[-3]) / 2
