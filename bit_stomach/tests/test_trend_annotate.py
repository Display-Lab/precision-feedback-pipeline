
from unittest.mock import Mock
import trend_annotate
import pandas as pd
from pandas.testing 


def test_find_number():
    #create test data
    #test data1
    back_up_df= pd.DataFrame(columns=['measure', 'month', 'peer_average_comparator',
       'peer_90th_percentile_benchmark', 'peer_75th_percentile_benchmark',
       'Performance_Rate', 'goal_comparison_value'], 
                  index = [1, 2, 3])
    back_up_df.loc[1] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
    back_up_df.loc[2] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
    back_up_df.loc[3] = ["BP03","2023-12-01",85,88,96,0.85,0.90]
    #test data2
    back_up_df1= pd.DataFrame(columns=['measure', 'month', 'peer_average_comparator',
       'peer_90th_percentile_benchmark', 'peer_75th_percentile_benchmark',
       'Performance_Rate', 'goal_comparison_value'], 
                  index = [1, 2, 3])
    back_up_df1.loc[1] = ["BP03","2023-11-01",85,88,96,0.80,0.90]
    back_up_df1.loc[2] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
    back_up_df1.loc[3] = ["BP03","2023-12-01",85,88,96,0.95,0.90]
    #testdata3
    back_up_df2= pd.DataFrame(columns=['measure', 'month', 'peer_average_comparator',
       'peer_90th_percentile_benchmark', 'peer_75th_percentile_benchmark',
       'Performance_Rate', 'goal_comparison_value'], 
                  index = [1, 2, 3])
    back_up_df2.loc[1] = ["BP03","2023-11-01",85,88,96,0.90,0.90]
    back_up_df2.loc[2] = ["BP03","2023-11-01",85,88,96,0.85,0.90]
    back_up_df2.loc[3] = ["BP03","2023-12-01",85,88,96,0.80,0.90]

   

    
    #test
    assert trend_annotate.find_number(back_up_df,"positive") == 0
    assert trend_annotate.find_number(back_up_df1,"positive") == 2
    assert trend_annotate.find_number(back_up_df2,"negative") == 2