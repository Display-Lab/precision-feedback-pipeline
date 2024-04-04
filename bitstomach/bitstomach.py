import pandas as pd
from rdflib import RDF, BNode, Graph

from bitstomach.signals import SIGNALS
from utils.namespace import PSDO, SLOWMO


def extract_signals(performance_data) -> Graph:
    """
    Prepares performance data, loops through measures and calls each signal detect method,
    adds the measure to the signal and adds each signal to the graph as motivating information
    """
    # create the graph
    g = Graph()
    r = g.resource(BNode("performance_content"))
    r.set(RDF.type, PSDO.performance_content)

    if not performance_data:
        return g
    else:
        # TODO: implement a million datarules and maybe business
        performance_df = fix_up(performance_data)

    measures = performance_df["measure"].unique()
    for measure in measures:
        for signal_type in SIGNALS:
            signals = signal_type.detect(
                performance_df[performance_df["measure"].isin([measure])]
            )
            if not signals:
                continue

            for s in signals:
                s.add(SLOWMO.RegardingMeasure, BNode(measure))
                r.add(PSDO.motivating_information, s.identifier)
                g += s.graph
    return g


def fix_up(performance_data):
    performance_df = pd.DataFrame(performance_data[1:], columns=performance_data[0])

    performance_df = performance_df[performance_df["denominator"] >= 10]
    performance_df.rename(
        columns={"MPOG_goal": "goal_comparator_content"}, inplace=True
    )
    performance_df["passed_rate"] = (
        performance_df["passed_count"] / performance_df["denominator"]
    )

    return performance_df
