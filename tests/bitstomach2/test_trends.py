import pandas as pd
import pytest

from bitstomach2.signals import Trend
from bitstomach2.signals._trend import _detect

## Trend resource
def test_empty_perf_data_raises_value_error():
    with pytest.raises(ValueError):
        Trend.detect(pd.DataFrame())
        
def test_no_trend_returns_none():
    mi = Trend.detect(
        pd.DataFrame(
            [
                [90],
                [90],
                [90]
            ], 
            columns=["passed_percentage"] 
        )
    )    
    assert mi is None
    
    
## Signal detection tests
def test_trend_is_detected():
    slope = _detect(
        pd.DataFrame(
            columns=["passed_percentage"], 
            data=[[90],
                  [91],
                  [92]] 
        )
    )
    
    assert slope == 1
    
