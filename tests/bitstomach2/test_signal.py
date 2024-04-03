from rdflib import RDF, BNode, Graph

from bitstomach2.signals import Comparison, Signal, Trend
from utils.namespace import PSDO, SLOWMO

def test_is_rdf_type_of():
    mi = Graph().resource(BNode())
    mi[RDF.type] = PSDO.performance_gap_content

    comparison = Comparison()

    assert comparison.is_rdf_type_of(mi)
    
    mi.add(RDF.type, PSDO.motivating_information)
    
    assert comparison.is_rdf_type_of(mi)

def test_signal_for_type():
    mi = Graph().resource(BNode())
    mi[RDF.type] = PSDO.performance_gap_content
    
    assert Signal.for_type(mi) == Comparison

    mi.add(RDF.type, PSDO.motivating_information)
    
    assert Signal.for_type(mi) == Comparison
    
    signal = Signal.for_type(mi)
    
    assert signal.signal_type == PSDO.performance_gap_content
    
def test_comparison_dispositions():
    
    g = Graph()
    mi = g.resource(BNode())
    
    mi[RDF.type] = PSDO.performance_gap_content
    mi.add(RDF.type, PSDO.motivating_information)
    
    mi[SLOWMO.RegardingComparator] = BNode()
    mi.value(SLOWMO.RegardingComparator)[RDF.type] = PSDO.peer_90th_percentile_benchmark

    signal = Signal.for_type(mi)
    assert signal == Comparison
    
    assert g.resource(PSDO.peer_90th_percentile_benchmark) in signal.disposition(mi)
    
    
def test_trend_dispositions():
    g = Graph()
    mi = g.resource(BNode())

    mi[RDF.type] = PSDO.performance_trend_content
    mi.add(RDF.type, PSDO.motivating_information)

    signal = Signal.for_type(mi)
    
    assert signal == Trend

    dispos = signal.disposition(mi)
    assert g.resource(PSDO.performance_trend_content) in dispos
    assert g.resource(PSDO.motivating_information) in dispos
    assert g.resource(PSDO.peer_90th_percentile_benchmark) not in dispos


def test_wrong_signal():
    g = Graph()
    mi = g.resource(BNode())

    mi[RDF.type] = PSDO.performance_trend_content
    mi.add(RDF.type, PSDO.motivating_information)

    signal = Comparison

    dispos = signal.disposition(mi)
    
    assert not dispos
