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
    # else
    #     performance_df = fix_up(performance_data)

    performance_df = pd.DataFrame(performance_data[1:], columns=performance_data[0])

    measures = performance_df["measure"].unique()

    for measure in measures:
        signal = Comparison()
        signals = signal.detect(
            to_perf_dict(
                performance_df[performance_df['measure'].isin([measure])]
                )
        )

        for s in signals:
            r.add(URIRef("motivating_information"), s.identifier)
            g += s.graph
    return g


def to_perf_dict(mpdf: pd.DataFrame):
    # mpdf: pd.DataFrame = pdf[pdf["measure"].isin([measure])]
    
    mpdf["levels"] = mpdf["passed_count"] / mpdf["denominator"]/100.0

    # perf_dict template
    perf_dict = {"levels": [], "comparators": {}}

    # add the levels 
    perf_dict['levels'] = mpdf["levels"].to_list()
    
    # add the comps
    mpdf.rename(columns={"MPOG_goal": "goal_comparator_content"},inplace=True)
    comp_cols = [
        "peer_average_comparator",
        "peer_75th_percentile_benchmark",
        "peer_90th_percentile_benchmark",
        "goal_comparator_content"
    ]
    perf_dict['comparators'] = mpdf[-1:][comp_cols].to_dict(orient='records')[0]

    return perf_dict
    # {
    #     "levels": [0.7, 0.8, 0.9],
    #     "comparators": {
    #         "peer_average_comparator": 0,
    #         "peer_75th_percentile_benchmark": 0.89,
    #         "peer_90th_percentile_benchmark": 0.91,
    #         "goal_comparator_content": 1.0,
    #     },
    # }


# get_performance_for_measure performance_df, measure returns
# {"levels": [0.7, 0.8, 0.9], "comparators": {"peer_average_comparator":0.85, "peer_75th_percentile_benchmark":0.89, "peer_90th_percentile_benchmark":0.91, "goal_comparator_content":1.0}}
