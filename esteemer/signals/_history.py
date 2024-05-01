from typing import List, Optional

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
            .tail(12)
            .sort_index()
        )

        recurrence = History._detect(history)

        return [History._resource(recurrence)]

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
                signal.value(URIRef("recurrence_count")).value / 11, 4
            )
            mods.append(history_dict)

        return mods

    @staticmethod
    def _detect(history: pd.DataFrame) -> float:
        return (
            history[history.index != "current_month"]["message_template"]
            == history.loc["current_month", "message_template"]
        ).sum()

    @staticmethod
    def to_element(candidate: Resource):
        element = {}
        element["message_template"] = str(
            candidate.value(SLOWMO.AncestorTemplate).identifier
        )
        element["acceptable_by"] = candidate.value(SLOWMO.AcceptableBy).value

        return {"current_month": element}
