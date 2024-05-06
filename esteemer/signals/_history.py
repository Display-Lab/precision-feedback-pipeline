from typing import List, Optional

import numpy as np
import pandas as pd
from rdflib import XSD, Literal, URIRef
from rdflib.resource import Resource

from bitstomach.signals import Signal
from utils.namespace import SLOWMO


class History(Signal):
    # TODO: Allow an array of types
    signal_type = SLOWMO.MessageRecurrance

    @staticmethod
    def detect(message_history: dict) -> Optional[List[Resource]]:
        if not message_history:
            return None

        history = (
            pd.DataFrame.from_dict(message_history, orient="index")
            .tail(12 + 1)
            .sort_index()
        )

        message_recurrence, message_recency, measure_recurrence, measure_recency = (
            History._detect(history)
        )

        return [History._resource(message_recurrence)]

    @classmethod
    def _resource(cls, recurrence_count: int) -> Resource:
        base = super()._resource()

        base[URIRef("recurrence_count")] = Literal(
            recurrence_count, datatype=XSD.integer
        )
        return base

    @classmethod
    def moderators(cls, signals: List[Resource]) -> List[dict]:
        mods = []

        for signal in super().select(signals):
            history_dict = {}
            history_dict["recurrence_count"] = round(
                signal.value(URIRef("recurrence_count")).value / 12, 4
            )
            mods.append(history_dict)

        return mods

    @staticmethod
    def _detect(history: pd.DataFrame) -> float:
        message_recurrence_map = (
            history[history.index != "current_month"]["message_template"]
            == history.loc["current_month", "message_template"]
        ).values

        message_count = message_recurrence_map.sum()

        message_recency = (
            np.argmax(message_recurrence_map[::-1] > 0)
            if any(message_recurrence_map)
            else len(message_recurrence_map)
        ) + 1

        measure_recurrence_map = (
            history[history.index != "current_month"]["measure"]
            == history.loc["current_month", "measure"]
        ).values

        measure_count = measure_recurrence_map.sum()

        measure_recency = (
            np.argmax(measure_recurrence_map[::-1] > 0)
            if any(measure_recurrence_map)
            else len(measure_recurrence_map)
        ) + 1

        return message_count, message_recency, measure_count, measure_recency

    @staticmethod
    def to_element(candidate: Resource):
        element = {}
        element["message_template"] = str(
            candidate.value(SLOWMO.AncestorTemplate).identifier
        )
        element["acceptable_by"] = candidate.value(SLOWMO.AcceptableBy).value
        element["measure"] = str(candidate.value(SLOWMO.RegardingMeasure).identifier)

        return {"current_month": element}
