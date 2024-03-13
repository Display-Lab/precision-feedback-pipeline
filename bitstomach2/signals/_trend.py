from typing import List, Optional
import pandas as pd
from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from utils import PSDO, SLOWMO


class Trend():
    
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
        
        
def _resource(slope):
    base = Graph().resource(BNode()) 
    base[RDF.type] = PSDO.performance_trend_content 
    base[SLOWMO.PerformanceTrendSlope] = Literal(slope)
    return base
    
def _detect(perf_data):
    performance_rates = perf_data["passed_percentage"]
    last_index = len(performance_rates) - 1
    change_this_month = (
        performance_rates[last_index] - performance_rates[last_index - 1]
    )
    change_last_month = (
        performance_rates[last_index - 1] - performance_rates[last_index - 2]
    )

    if change_this_month * change_last_month < 0:
        return 0

    return (performance_rates[last_index] - performance_rates[last_index - 2]) / 2