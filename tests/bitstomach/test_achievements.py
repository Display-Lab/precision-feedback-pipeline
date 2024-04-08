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
    assert signals is None


def test_signal_properties(perf_data):
    signals = Achievement.detect(perf_data)
    assert isinstance(signals[0], Resource)

    slope = signals[0].value(SLOWMO.PerformanceTrendSlope).value
    assert slope == pytest.approx(0.01)

    gap = signals[0].value(SLOWMO.PerformanceGapSize).value
    assert gap == pytest.approx(0.17)


perf_level_test_set = [
    ([0.65, 0.70, 0.75], 0.05, -0.05, PSDO.peer_average_comparator),
    ([0.60, 0.70, 0.80], 0.1, 0, PSDO.peer_average_comparator),
    ([0.62, 0.72, 0.82], 0.1, 0.02, PSDO.peer_average_comparator),
]


@pytest.mark.parametrize("perf_level, slope, gap, comparator", perf_level_test_set)
def test_signal_properties2(perf_level, slope, gap, comparator, perf_data):
    perf_data2 = perf_data.assign(passed_rate=perf_level)
    signals = Achievement.detect(perf_data2)

    assert len(signals) == 4

    signal = signals[0]
    assert signal.value(SLOWMO.PerformanceTrendSlope).value == pytest.approx(slope)
    assert signal.value(SLOWMO.PerformanceGapSize).value == pytest.approx(gap)
    assert signal.value(SLOWMO.RegardingComparator).identifier == comparator


# detection_test_set = [
#     ([0.77, 0.88, 0.99], 0.11, "simple positive trend"),
#     ([0.99, 0.88, 0.77], -0.11, "simple negative trend"),
#     ([0.88, 0.88, 0.88], 0.0, "no trend"),
#     ([0.77, 0.77, 0.99], 0.11, "partial positive trend"),
#     ([0.77, 0.99, 0.99], 0.0, "partial positive trend"),
#     ([0.77, 0.99, 0.88], 0.0, "non-monotonic, last month negative"),
#     ([0.88, 0.77, 0.88], 0.0, "non-monotonic, last month positive"),
# ]
# @pytest.mark.parametrize("perf_level, expected, condition", detection_test_set)
# def test_trend__detect(perf_level: list, expected: float, condition: str):
#     perf = pd.DataFrame({"passed_rate": perf_level})
#     slope = Trend._detect(perf)
#     assert slope == pytest.approx(expected), condition + " failed"


# mods_test_set = [
#     (0.11, round(abs(0.11), 4), "simple negative trend"),
#     (-0.111111111111, round(abs(0.111111111111), 4), "simple negative trend"),
#     (0.0, 0.0, "no trend"),
# ]


# @pytest.mark.parametrize("slope, moderator, condition", mods_test_set)
# def test_trend_moderators(slope: float, moderator: float, condition):
#     signal = Trend._resource(slope)
#     mods = Trend.moderators([signal])[0]

#     assert str(mods["trend_size"]) == str(moderator), condition + " failed"
