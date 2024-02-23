import unittest
from unittest.mock import patch, Mock
from bit_stomach import trend_annotate,prepare_data_annotate
import pandas as pd
import json
import rdflib
from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.serializer import Serializer
import numpy as np
#The trend annotation happens only when there is difference between last two time intervals. If there is no difference between last two time intervals, the trend annotation does not happen
def test_theil_reg():
        # create test data
        # test data 1
        back_up_df = pd.DataFrame(
            columns=[
                "measure",
                "month",
                "peer_average_comparator",
                "peer_90th_percentile_benchmark",
                "peer_75th_percentile_benchmark",
                "Performance_Rate",
                "goal_comparison_value",
            ],
            index=[1, 2, 3],
        )
        back_up_df.loc[1] = ["BP03", "2023-10-01", 85, 88, 96, 0.85, 0.90]
        back_up_df.loc[2] = ["BP03", "2023-11-01", 87, 88, 96, 0.87, 0.90]
        back_up_df.loc[3] = ["BP03", "2023-12-01", 90, 88, 96, 0.90, 0.90]

        xcol = "month"
        ycol = "Performance_Rate"
        back_up_df["month"] = back_up_df["month"].astype("datetime64")

        # test data 2
        back_up_df1 = pd.DataFrame(
            columns=[
                "measure",
                "month",
                "peer_average_comparator",
                "peer_90th_percentile_benchmark",
                "peer_75th_percentile_benchmark",
                "Performance_Rate",
                "goal_comparison_value",
            ],
            index=[1, 2, 3],
        )
        back_up_df1.loc[1] = ["BP03", "2023-10-01", 85, 88, 96, 0.85, 0.90]
        back_up_df1.loc[2] = ["BP03", "2023-11-01", 87, 88, 96, 0.85, 0.90]
        back_up_df1.loc[3] = ["BP03", "2023-12-01", 90, 88, 96, 0.85, 0.90]

        xcol = "month"
        ycol = "Performance_Rate"
        back_up_df1["month"] = back_up_df1["month"].astype("datetime64")

        # test data 3
        back_up_df2 = pd.DataFrame(
            columns=[
                "measure",
                "month",
                "peer_average_comparator",
                "peer_90th_percentile_benchmark",
                "peer_75th_percentile_benchmark",
                "Performance_Rate",
                "goal_comparison_value",
            ],
            index=[1, 2, 3],
        )
        back_up_df2.loc[1] = ["BP03", "2023-10-01", 85, 88, 96, 0.85, 0.90]
        back_up_df2.loc[2] = ["BP03", "2023-11-01", 85, 88, 96, 0.82, 0.90]
        back_up_df2.loc[3] = ["BP03", "2023-12-01", 85, 88, 96, 0.80, 0.90]

        xcol = "month"
        ycol = "Performance_Rate"
        back_up_df2["month"] = back_up_df2["month"].astype("datetime64")

        # test data 4
        back_up_df = pd.DataFrame(
            columns=[
                "measure",
                "month",
                "peer_average_comparator",
                "peer_90th_percentile_benchmark",
                "peer_75th_percentile_benchmark",
                "Performance_Rate",
                "goal_comparison_value",
            ],
            index=[1, 2, 3],
        )
        back_up_df.loc[1] = ["BP03", "2023-10-01", 85, 88, 96, 0.85, 0.90]
        back_up_df.loc[2] = ["BP03", "2023-11-01", 87, 88, 96, 0.87, 0.90]
        back_up_df.loc[3] = ["BP03", "2023-12-01", 90, 88, 96, 0.90, 0.90]

        xcol = "month"
        ycol = "Performance_Rate"
        back_up_df["month"] = back_up_df["month"].astype("datetime64")


        # call method of test
        out = trend_annotate.theil_reg(back_up_df, xcol, ycol)
        trend_slope = out[0]

        out1 = trend_annotate.theil_reg(back_up_df1, xcol, ycol)
        trend_slope1 = out1[0]
        # print(out1)

        out2 = trend_annotate.theil_reg(back_up_df2, xcol, ycol)
        trend_slope2 = out2[0]
        # print(out2)

        # expected output
        expected_output = 9.486945962355806e-18
        expected_output1 = 0
        expected_output2 = -9.486945962355786e-18

        # assert whether resulted output equals expected output
        assert trend_slope == expected_output
        # assert second data output is correct
        assert trend_slope1 == expected_output1
        # asser third data output is correct
        assert trend_slope2 == expected_output2


    