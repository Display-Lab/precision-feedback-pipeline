from rdflib import RDF, BNode, Graph, URIRef
from utils.namespace import PSDO
import pandas as pd
from bitstomach2.signals import Comparison

def extract_signals(performance_data) -> Graph:
    performance_df = pd.DataFrame(performance_data[1:], columns=performance_data[0])
    
    g= Graph()
    
    r = g.resource(BNode("performance_content"))
    r.set(RDF.type, PSDO.performance_content)
    
    
    measures = performance_df['measure'].unique()
    
    for measure in measures: 
        signal = Comparison()
        signals = signal.detect({"levels": [0.7, 0.8, 0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89, "peer_90th_percentile_benchmark":0.91, "goal_comparator_content":1.0}})

        for s in signals:
            r.add(URIRef("motivating_information"), s.identifier)
            g += s.graph
    return g

#get_performance_for_measure performance_df, measure returns
    #{"levels": [0.7, 0.8, 0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89, "peer_90th_percentile_benchmark":0.91, "goal_comparator_content":1.0}}