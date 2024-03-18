from typing import List, Optional

import pandas as pd
from rdflib import XSD, BNode, Graph, Literal, URIRef
from rdflib.resource import Resource

from bitstomach2.signals import Signal


class History(Signal):
    # TODO: Allow an array of types
    signal_type = "History"

    @staticmethod
    def detect(message_history: dict) -> Optional[List[Resource]]:
        if not message_history:
            return None

        history = pd.DataFrame.from_dict(message_history, orient="index")

        history = history.sort_index()
        occurance = History._detect(history)

        return [History._resource(occurance)]

    @classmethod
    def _resource(cls, occurance: int) -> Resource:
        base = Graph().resource(BNode())
        base[URIRef("occurance")] = Literal(occurance, datatype=XSD.integer)
        return base

    @classmethod
    def moderators(cls, signals: List[Resource]) -> List[dict]:
        mods = []

        for signal in signals:
            history_dict = {}
            history_dict["occurance"] = signal.value(URIRef("occurance")).value
            mods.append(history_dict)

        return mods

    @staticmethod
    def _detect(history: pd.DataFrame) -> float:
        return (
            history[history.index != "current_month"]["template"]
            == history.loc["current_month", "template"]
        ).sum()
