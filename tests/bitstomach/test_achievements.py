import pandas as pd
import pytest
from rdflib import RDF, BNode, Graph
from rdflib.resource import Resource

from bitstomach.signals import Achievement
from utils.namespace import PSDO, SLOWMO


@pytest.fixture
def perf_data() -> pd.DataFrame:
    performance_data = [
        [
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
        [157, "BP01", "2022-08-01", 0.95, 90.0, 0, 100.0, 85.0, 88.0, 90.0, 99.0],
        [157, "BP01", "2022-09-01", 0.96, 91.0, 0, 100.0, 85.0, 89.0, 91.0, 100.0],
        [157, "BP01", "2022-09-01", 0.97, 92.0, 0, 100.0, 80.0, 85.0, 90.0, 95.0],
    ]
    return pd.DataFrame(performance_data[1:], columns=performance_data[0])


def test_achievement_is_rdf_type():
    g: Graph = Graph()
    mi = g.resource(BNode())
    mi.add(RDF.type, PSDO.achievement_content)

    assert Achievement.is_rdf_type_of(mi)


def test_disposition():
    g: Graph = Graph()
    mi = g.resource(BNode())
    mi.add(RDF.type, PSDO.achievement_content)

    dispositions = Achievement.disposition(mi)
    assert len(dispositions)
    assert g.resource(PSDO.achievement_content) in dispositions


def test_detect_handles_empty_datframe():
    with pytest.raises(ValueError):
        Achievement.detect(pd.DataFrame())


def test_detect_returns_mi(perf_data):
    perf_data["passed_rate"] = [0.94, 0.96, 0.95]
    signals = Achievement.detect(perf_data)
    assert signals == []


def test_signal_properties(perf_data):
    signals = Achievement.detect(perf_data)
    assert isinstance(signals[0], Resource)

    slope = signals[0].value(SLOWMO.PerformanceTrendSlope).value
    assert slope == pytest.approx(0.01)

    gap = signals[0].value(SLOWMO.PerformanceGapSize).value
    assert gap == pytest.approx(0.02)


perf_level_test_set = [
    (
        [0.67, 0.79, 0.97],
        [80.0, 85.0, 90.0, 95.0],
        {
            PSDO.peer_average_comparator,
            PSDO.peer_75th_percentile_benchmark,
            PSDO.peer_90th_percentile_benchmark,
            PSDO.goal_comparator_content,
        },
        "achievement all benchmarks",
    ),
    (
        [0.67, 0.95, 0.99],
        [80.0, 96.0, 98.0, 97.0],
        {
            PSDO.peer_75th_percentile_benchmark,
            PSDO.peer_90th_percentile_benchmark,
            PSDO.goal_comparator_content,
        },
        "achievement no peer_90th_percentile_benchmark",
    ),
    (
        [0.67, 0.96, 0.97],
        [80.0, 98.0, 96.5, 95.0],
        {
            PSDO.peer_90th_percentile_benchmark,
            # PSDO.goal_comparator_content,
        },
        "last month negative gap for 90 percentile",
    ),
]


@pytest.mark.parametrize(
    "perf_level, comparator_values, types, condition", perf_level_test_set
)
def test_detect(perf_level, comparator_values, types: dict, condition, perf_data):
    perf_data2 = perf_data.assign(passed_rate=perf_level)

    perf_data2.iloc[:, -4:] = comparator_values

    signals = Achievement.detect(perf_data2)

    comparators = {s.value(SLOWMO.RegardingComparator).identifier for s in signals}

    assert comparators == types
