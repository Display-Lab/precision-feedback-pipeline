import pandas as pd


class Trend():
    
    @staticmethod
    def detect(perf_data: pd.DataFrame):
        if perf_data.empty:
            raise ValueError
        
        if perf_data["passed_percentage"].count() < 3:
            return None
        
        slope = _detect(perf_data)
        
        return slope if slope else None
    
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