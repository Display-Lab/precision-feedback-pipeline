import pandas as pd
from rdflib import RDF, BNode, Graph, URIRef

from bitstomach2.signals import Comparison
from utils.namespace import PSDO


def extract_signals(performance_data) -> Graph:
    # create the graph
    g = Graph()
    r = g.resource(BNode("performance_content"))
    r.set(RDF.type, PSDO.performance_content)

    if not performance_data:
        return g
    else:
        performance_df = fix_up(performance_data)

    measures = performance_df["measure"].unique()

    for measure in measures:
        signal = Comparison()
        signals = signal.detect(            
                performance_df[performance_df['measure'].isin([measure])]                
        )

        for s in signals:
            r.add(URIRef("motivating_information"), s.identifier)
            g += s.graph
    return g


def fix_up(performance_data):
    performance_df = pd.DataFrame(performance_data[1:], columns=performance_data[0])
    
    performance_df = performance_df[performance_df['denominator'] >= 10]
    performance_df.rename(columns={"MPOG_goal": "goal_comparator_content"},inplace=True)
    performance_df["passed_percentage"] = performance_df["passed_count"] / performance_df["denominator"] * 100.0
    
    return performance_df
    
