import pandas as pd
from rdflib import RDF, BNode, Graph

from bitstomach.signals import SIGNALS
from utils.namespace import PSDO, SLOWMO


def extract_signals(performance_df: pd.DataFrame) -> Graph:
    """
    Prepares performance data, loops through measures and calls each signal detect method,
    adds the measure to the signal and adds each signal to the graph as motivating information
    """
    # create the graph
    g = Graph()
    r = g.resource(BNode("performance_content"))
    r.set(RDF.type, PSDO.performance_content)

    if performance_df.empty:
        return g
    else:
        # TODO: implement a million datarules and maybe business
        performance_df = fix_up(performance_df)

    for measure in performance_df.attrs["measures"]:
        measure_rows = performance_df[performance_df["measure"].isin([measure])]
        if performance_df.attrs["performance_month"] not in measure_rows["month"].values:
            continue
            
        for signal_type in SIGNALS:

            signals = signal_type.detect(
                measure_rows
            )
            if not signals:
                continue

            for s in signals:
                s.add(SLOWMO.RegardingMeasure, BNode(measure))
                r.add(PSDO.motivating_information, s.identifier)
                g += s.graph
    return g


def fix_up(performance_df:pd.DataFrame):
    # performance_df = pd.DataFrame(performance_data[1:], columns=performance_data[0])

    performance_df = performance_df[performance_df["denominator"] >= 10]

    performance_df.rename(
        columns={"MPOG_goal": "goal_comparator_content"}, inplace=True
    )
    performance_df["passed_rate"] = (
        performance_df["passed_count"] / performance_df["denominator"]
    )

    performance_df.attrs["measures"] = performance_df["measure"].unique()
    #performance_df.attrs["valid_measures"] = performance_df["measure"].unique()
    return performance_df
