import pandas as pd
import pytest
from rdflib.resource import Resource
from rdflib import RDF, Literal
from utils import PSDO, SLOWMO

from bitstomach2.signals import Trend
from bitstomach2.signals._trend import _detect


## Trend resource
def test_empty_perf_data_raises_value_error():
    with pytest.raises(ValueError):
        Trend.detect(pd.DataFrame())


def test_no_trend_returns_none():
    mi = Trend.detect(
        pd.DataFrame(
            {"passed_percentage": [90, 90, 90]},
        )
    )
    assert mi is None


## Signal detection tests
def test_trend_is_detected():
    slope = _detect(
        pd.DataFrame(columns=["passed_percentage"], data=[[90], [91], [92]])
    )
    assert slope == 1

    slope = _detect(
        pd.DataFrame(columns=["passed_percentage"], data=[[90], [92], [94]])
    )
    assert slope == 2

    slope = _detect(
        pd.DataFrame(columns=["passed_percentage"], data=[[90], [92], [90], [92], [94]])
    )
    assert slope == 2


def test_trend_as_resource():
    signal = Trend.detect(
        pd.DataFrame(columns=["passed_percentage"], data=[[90], [91], [92]])
    ).pop()

    assert isinstance(signal,Resource)

    assert signal.value(RDF.type).identifier == PSDO.performance_trend_content
    assert signal.value(SLOWMO.PerformanceTrendSlope) == Literal(1.0)
