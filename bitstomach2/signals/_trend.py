from typing import List, Optional

import pandas as pd
from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from utils import PSDO, SLOWMO


class Trend:
    @staticmethod
    def detect(perf_data: pd.DataFrame) -> Optional[List[Resource]]:
        if perf_data.empty:
            raise ValueError

        if perf_data["passed_percentage"].count() < 3:
            return None

        slope = _detect(perf_data)

        if not slope:
            return None

        return [_resource(slope)]

    @staticmethod
    def to_moderators(motivating_informations: List[Resource]):
        motivating_info_dict: dict = {}

        if not motivating_informations:
            return motivating_info_dict
        for mi in motivating_informations:
            if PSDO.performance_trend_content not in [
                t.identifier for t in mi.objects(RDF.type)
            ]:
                continue
            motivating_info_dict["trend_size"] = mi.value(
                SLOWMO.PerformanceTrendSlope
            ).value

            motivating_info_dict["type"] = []
            for trend_type in list(mi[RDF.type]):
                motivating_info_dict["type"].append(trend_type.identifier)

            break
        return motivating_info_dict

    @staticmethod
    def select(motivating_informations: List[Resource]) -> List[Resource]:
        result = []
        for mi in motivating_informations:
            if PSDO.performance_trend_content in [
                t.identifier for t in mi.objects(RDF.type)
            ]:
                result.append(mi)

        return result


def _resource(slope):
    base = Graph().resource(BNode())
    base.add(RDF.type, PSDO.performance_trend_content)
    if slope > 0:
        base.add(RDF.type, PSDO.positive_performance_trend_content)
    elif slope < 0:
        base.add(RDF.type, PSDO.negative_performance_trend_content)

    base[SLOWMO.PerformanceTrendSlope] = Literal(slope)
    return base


def _detect(perf_data):
    performance_rates = perf_data["passed_percentage"]
    change_this_month = performance_rates.iloc[-1] - performance_rates.iloc[-2]
    change_last_month = performance_rates.iloc[-2] - performance_rates.iloc[-3]

    if change_this_month * change_last_month < 0:
        return 0

    return (performance_rates.iloc[-1] - performance_rates.iloc[-3]) / 2
