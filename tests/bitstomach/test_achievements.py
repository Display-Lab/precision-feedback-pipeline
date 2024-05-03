from typing import List

import pandas as pd
import pytest
from rdflib import RDF, BNode, Graph, Literal
from rdflib.resource import Resource

from bitstomach.signals import Achievement
from utils.namespace import PSDO, SLOWMO


@pytest.fixture
def perf_data() -> pd.DataFrame:
    performance_data = [
        [
            "valid",
            "staff_number",
            "measure",
            "month",
            "passed_rate",
            "passed_count",
            "flagged_count",
            "denominator",
            "peer_average_comparator",
            "peer_75th_percentile_benchmark",
            "peer_90th_percentile_benchmark",
            "goal_comparator_content",
        ],
        [True, 157, "BP01", "2022-08-01", 0.85, 90.0, 0, 100.0, 85.0, 88.0, 90.0, 99.0],
        [
            True,
            157,
            "BP01",
            "2022-09-01",
            0.86,
            91.0,
            0,
            100.0,
            85.0,
            89.0,
            91.0,
            100.0,
        ],
        [True, 157, "BP01", "2022-10-01", 0.97, 92.0, 0, 100.0, 80.0, 85.0, 90.0, 95.0],
    ]
    df = pd.DataFrame(performance_data[1:], columns=performance_data[0])
    df.attrs["performance_month"] = "2022-10-01"
    return df


def test_achievement_is_rdf_type():
    g: Graph = Graph()
    mi = g.resource(BNode())
    mi.add(RDF.type, PSDO.achievement_content)

    assert Achievement.is_rdf_type_of(mi)


def test_disposition():
    g: Graph = Graph()

    # Hand create an Achievement with dispositions
    mi: Resource = g.resource(BNode())
    mi.add(RDF.type, PSDO.achievement_content)
    mi.add(RDF.type, PSDO.performance_gap_content)
    mi.add(RDF.type, PSDO.performance_trend_content)

    c = mi.graph.resource(BNode())  # Comparator
    c.add(RDF.type, PSDO.goal_comparator_content)
    mi[SLOWMO.RegardingComparator] = c

    dispositions = Achievement.disposition(mi)
    assert len(dispositions)
    assert g.resource(PSDO.achievement_content) in dispositions


def test_detect_handles_empty_datframe():
    with pytest.raises(ValueError):
        Achievement.detect(pd.DataFrame())


def test_signal_properties(perf_data):
    signals = Achievement.detect(perf_data)
    assert isinstance(signals[0], Resource)

    slope = signals[0].value(SLOWMO.PerformanceTrendSlope).value
    assert slope == pytest.approx(0.06)

    gap = signals[0].value(SLOWMO.PerformanceGapSize).value
    assert gap == pytest.approx(0.12)

    gap = signals[0].value(SLOWMO.PriorPerformanceGapSize).value
    assert gap == pytest.approx(-0.03)


perf_level_test_set = [
    (
        [0.67, 0.79, 0.97],
        [80.0, 85.0, 90.0, 95.0],
        {
            PSDO.peer_90th_percentile_benchmark,
            PSDO.peer_75th_percentile_benchmark,
            PSDO.peer_average_comparator,
            PSDO.goal_comparator_content,
        },
        "achievement all benchmarks",
    ),
    (
        [0.67, 0.95, 0.99],
        [80.0, 96.0, 98.0, 97.0],
        {
            PSDO.peer_90th_percentile_benchmark,
            PSDO.peer_75th_percentile_benchmark,
            PSDO.goal_comparator_content,
        },
        "achievement no peer_average_comparator",
    ),
    (
        [0.67, 0.96, 0.97],
        [80.0, 95.0, 96.5, 95.0],
        {
            PSDO.peer_90th_percentile_benchmark,
        },
        "last month negative gap for 90 percentile",
    ),
    (
        [0.67, 0.98, 0.97],
        [80.0, 95.0, 96.5, 95.0],
        set(),
        "no trend",
    ),
]


@pytest.mark.parametrize(
    "perf_level, comparator_values, types, condition", perf_level_test_set
)
def test_detect_signals(perf_level, comparator_values, types, condition, perf_data):
    perf_data2 = perf_data.assign(passed_rate=perf_level)

    perf_data2.iloc[:, -4:] = comparator_values

    signals = Achievement.detect(perf_data2)

    comparators = {
        s.value(SLOWMO.RegardingComparator / RDF.type).identifier for s in signals
    }

    assert comparators == types, condition + " failed"
    

def test_detect(perf_data):
    g: Graph = Graph()
    comparator = g.resource(BNode( ))
    comparator[RDF.type] = PSDO.peer_90th_percentile_benchmark
    streap_length = Achievement._detect(perf_data,comparator) 
    assert streap_length == 2
    
    new_row = pd.DataFrame({'passed_rate': [0.81],'peer_90th_percentile_benchmark': 90.0 })
    perf_data = pd.concat([new_row, perf_data], ignore_index=True)
    streap_length = Achievement._detect(perf_data,comparator) 
    assert streap_length == 3
    
    new_row = pd.DataFrame({'passed_rate': [0.91],'peer_90th_percentile_benchmark': 90.0 })
    perf_data = pd.concat([new_row, perf_data], ignore_index=True)
    streap_length = Achievement._detect(perf_data,comparator) 
    assert streap_length == 3
    pass


def test_only_current_month_no_achievement(perf_data):
    assert [] == Achievement.detect(perf_data[-2:])  # Prior month but no trend
    assert [] == Achievement.detect(perf_data[-1:])  # only current month
    assert [] != Achievement.detect(perf_data[:])  # three months


def test_moderators_return_dictionary():
    assert isinstance(Achievement.moderators([]), List)


def test_moderators():
    gap = 0.02
    prior_gap = -0.03
    slope = 0.1
    graph = Graph()
    r = graph.resource(BNode())
    # add achievement types
    r.add(RDF.type, PSDO.performance_gap_content)
    r.add(RDF.type, PSDO.performance_trend_content)
    r.add(RDF.type, PSDO.achievement_content)

    # add achievement properites
    r.add(SLOWMO.PerformanceGapSize, Literal(gap))
    r.add(SLOWMO.PerformanceTrendSlope, Literal(slope))
    r.add(SLOWMO.PriorPerformanceGapSize, Literal(prior_gap))
    r.add(SLOWMO.StreakLength, Literal(3))
    r.add(SLOWMO.RegardingMeasure, BNode("PONV05"))

    # Add the comparator
    c = graph.resource(BNode())
    c.set(RDF.type, PSDO.peer_90th_percentile_benchmark)
    c.set(RDF.value, Literal(95.0))
    r.add(SLOWMO.RegardingComparator, c)

    moderators = Achievement.moderators([r])

    moderator = [
        moderator
        for moderator in moderators
        if moderator["comparator_type"] == PSDO.peer_90th_percentile_benchmark
    ][0]

    assert moderator["gap_size"] == abs(gap)
    assert moderator["trend_size"] == abs(slope) * 2
    assert moderator["prior_gap_size"] == abs(prior_gap)
