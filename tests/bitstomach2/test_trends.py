import pandas as pd
import pytest
from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from bitstomach2.signals import Comparison, Trend
from bitstomach2.signals._trend import _detect, _resource
from utils import PSDO, SLOWMO


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

    assert isinstance(signal, Resource)

    assert signal.value(RDF.type).identifier == PSDO.performance_trend_content
    assert signal.value(SLOWMO.PerformanceTrendSlope) == Literal(1.0)


def test_to_moderators_return_dictionary():
    assert isinstance(Trend.to_moderators([]), dict)


def test_to_moderators_return_dictionary1():
    r = Graph().resource(BNode())
    r.add(RDF.type, PSDO.performance_trend_content)
    r.add(SLOWMO.PerformanceTrendSlope, Literal(2.0))
    r.add(RDF.type, PSDO.performance_trend_content)
    r.add(RDF.type, PSDO.positive_performance_trend_content)

    r.add(SLOWMO.RegardingMeasure, BNode("PONV05"))

    trend = Trend.to_moderators([r])
    assert trend["trend_size"] == 2.0

    assert PSDO.performance_trend_content in trend["type"]
    assert PSDO.positive_performance_trend_content in trend["type"]


def test_resource_selects_pos_or_neg():
    r = _resource(3.0)
    types = [t.identifier for t in list(r[RDF.type])]
    assert PSDO.positive_performance_trend_content in types
    assert PSDO.negative_performance_trend_content not in types

    r = _resource(-1.0)
    types = [t.identifier for t in list(r[RDF.type])]
    assert PSDO.positive_performance_trend_content not in types
    assert PSDO.negative_performance_trend_content in types

    r = _resource(0.0)
    types = [t.identifier for t in list(r[RDF.type])]
    assert PSDO.positive_performance_trend_content not in types
    assert PSDO.negative_performance_trend_content not in types


def test_select():
    r1 = Comparison().detect(
        pd.DataFrame(
            columns=[
                "measure",
                "passed_percentage",
                "peer_average_comparator",
                "peer_75th_percentile_benchmark",
                "peer_90th_percentile_benchmark",
                "goal_comparator_content",
            ],
            data=[["PONV05", 80, 90, 90, 90, 90]],
        )
    )

    r2 = Trend.detect(
        pd.DataFrame(
            {"passed_percentage": [89, 90, 91]},
        )
    )

    mi = r1 + r2

    assert len(mi) == 5

    selected_mi = Trend.select(mi)
    assert len(selected_mi) == 1
    assert PSDO.performance_trend_content in [
        t.identifier for t in selected_mi[0][RDF.type]
    ]

    selected_mi = Trend.select(r1)
    assert len(selected_mi) == 0

    selected_mi = Trend.select([])
    assert len(selected_mi) == 0

    selected_mi = Trend.select(r2)
    assert len(selected_mi) == 1
    assert selected_mi == r2
