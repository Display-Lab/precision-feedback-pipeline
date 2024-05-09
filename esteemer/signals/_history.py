from datetime import datetime
from typing import List, Optional, Tuple

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
    def detect(message_history: dict, current_month:dict) -> Optional[List[Resource]]:
        if not message_history:
            return None

        history = (
            pd.DataFrame.from_dict(message_history, orient="index")
            .tail(12 + 1)
            .sort_index()
        )

        message_recurrence, message_recency, measure_recurrence, measure_recency = (
            History._detect2(message_history, current_month)
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
    def _detect1(history: pd.DataFrame) -> Tuple[float, float, float, float]:
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
    def _detect2(history: dict, current_month_dict: dict) -> Tuple[float, float, float, float]:
        message_count = 0
        message_recency = 0
        measure_count = 0
        measure_recency= 0
        
        
        current_month, history_element = list(current_month_dict.items())[0]
        message_template = history_element["message_template"]
        measure = history_element["measure"]
        most_recent_message = None
        most_recent_neasure = None
        for key, value in history.items():
            month = datetime.fromisoformat(key)
            if history[key]["message_template"] == message_template:
                message_count += 1
                most_recent_message = month
                
                
            if history[key]["measure"] == measure:
                measure_count += 1
                most_recent_measure = month
                
        # message_recency = 
    
                

            
            
        
        
        return message_count, message_recency, measure_count, measure_recency


    @staticmethod
    def to_element(candidate: Resource):
        element = {}
        element["message_template"] = str(
            candidate.value(SLOWMO.AncestorTemplate).identifier
        )
        element["acceptable_by"] = candidate.value(SLOWMO.AcceptableBy).value
        element["measure"] = str(candidate.value(SLOWMO.RegardingMeasure).identifier)

        return element
