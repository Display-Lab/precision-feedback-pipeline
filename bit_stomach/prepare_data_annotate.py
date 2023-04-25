import warnings
 

import pandas as pd
from rdflib import Graph, URIRef, BNode
from rdflib.namespace import RDF

#from calc_gaps_slopes import gap_calc,trend_calc,monotonic_pred,mod_collector
#from insert_annotate import insert_annotate
from bit_stomach.gap_annotate import goal_gap_annotate,peer_gap_annotate,top_10_gap_annotate,top_25_gap_annotate
from bit_stomach.acheivement_loss_annotate import goal_acheivementloss_annotate,peer_acheivementloss_annotate,top_10_acheivementloss_annotate,top_25_acheivementloss_annotate
from bit_stomach.consecutive_gap_annotate import goal_consecutive_annotate,peer_consecutive_annotate,top_10_consecutive_annotate,top_25_consecutive_annotate
from bit_stomach.trend_annotate import trend_annotate
from bit_stomach.monotinicity_annotate import monotonic_annotate
warnings.filterwarnings("ignore")

class Prepare_data_annotate:
    global latest_measure_df

    latest_measure_df = pd.DataFrame()
    
    measure_data1 = pd.DataFrame()
    measure_data2 = pd.DataFrame()
    def __init__(self,input_graph:Graph,performance_data:pd.DataFrame,comparison_values:pd.DataFrame):
        self.performance_data=performance_data
        self.comparison_vaues=comparison_values
        performance_rate =[]
        for rowIndex, row in self.performance_data.iterrows():
            if (row['passed_count']==0 and row['denominator']==0):
                performance_rate.append(0.0)
            else:
                performance_rate.append(row['passed_count']/row['denominator'])
        self.performance_data['Performance_Rate']=performance_rate
        self.performance_data['peer_average_comparator']=self.performance_data['peer_average_comparator']/100
        self.performance_data['peer_90th_percentile_benchmark']=self.performance_data['peer_90th_percentile_benchmark']/100
        self.performance_data['peer_75th_percentile_benchmark']=self.performance_data['peer_75th_percentile_benchmark']/100
        self.performance_data['month'] = pd.to_datetime(self.performance_data['month'])
        self.performance_data[['measure']] = self.performance_data[['measure']].astype(str)
        self.comparison_vaues[['measure']] = self.comparison_vaues[['measure']].astype(str)
        
        self.performance_data.measure = self.performance_data.measure.str.encode('utf-8')
        self.comparison_vaues.measure = self.comparison_vaues.measure.str.encode('utf-8')
        self.data=self.performance_data.merge(self.comparison_vaues, how='outer', on=['measure'])
        self.data["measure"]=self.data["measure"].str.decode(encoding="UTF-8")
        self.data[['peer_average_comparator']] = self.data[['peer_average_comparator']].astype(float)
        self.data[['peer_90th_percentile_benchmark']] = self.data[['peer_90th_percentile_benchmark']].astype(float)
        self.data[['peer_75th_percentile_benchmark']] = self.data[['peer_75th_percentile_benchmark']].astype(float)
        self.data[['Performance_Rate']] = self.data[['Performance_Rate']].astype(float)
        self.data[['goal_comparison_value']] = self.data[['goal_comparison_value']].astype(float)
        idx= self.data.groupby(['measure'])['month'].transform(max) == self.data['month']
        self.latest_measure = self.data[idx]
        
        
        #self.data.to_csv("final_df1.csv")
        self.input_graph=input_graph

    def prepare_data_measure_name(self,measure_name:str,**goal_dicts):
        global measure_data1
        measure_data1 = self.latest_measure[self.latest_measure['measure'] == measure_name]
        global measure_data2
        measure_data2 = self.data[self.data['measure'] == measure_name]
        ac=BNode(measure_name)
        global comparator_bnode
        comparator_bnode=goal_dicts.get(ac)
        
        return measure_data1,measure_data2,comparator_bnode
        #print(measure_data1)
        #self.measure_data2.to_csv("final_df1.csv")
        
        
        # print(self.dict)
        # #
    def insert_annotate(self,a):
        s12 = URIRef('http://example.com/app#display-lab')
        p12=URIRef('http://example.com/slowmo#IsAboutPerformer')
        o12=BNode('p1')
        a.add((s12,p12,o12))
        s13=BNode('p1')
        p13=RDF.type
        o13=URIRef("http://purl.obolibrary.org/obo/psdo_0000085")
        a.add((s13,p13,o13))
        return a,s13
    
    def gaol_gap_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = goal_gap_annotate(self.a,self.s13,measure_data1,comparator_bnode)
        return a

    def peer_gap_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = peer_gap_annotate(self.a,self.s13,measure_data1,comparator_bnode)
        return a
    
    def top_10_gap_annotate(self,measure_name:str,**top_10_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**top_10_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = top_10_gap_annotate(self.a,self.s13,measure_data1,comparator_bnode)
        return a
    def top_25_gap_annotate(self,measure_name:str,**top_10_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**top_10_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = top_25_gap_annotate(self.a,self.s13,measure_data1,comparator_bnode)
        return a


    def goal_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = trend_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a

    def peer_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = trend_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a
    
    def top_10_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = trend_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a

    def top_25_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = trend_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a

    
    
    def goal_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = goal_acheivementloss_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a

    def peer_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = peer_acheivementloss_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a  

    def top_10_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = top_10_acheivementloss_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a
    
    def top_25_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = top_25_acheivementloss_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a


    def goalconsecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = goal_consecutive_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a   

    def peerconsecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = peer_consecutive_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a

    def top_10consecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = top_10_consecutive_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a 
    def top_25consecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = top_25_consecutive_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a 

    def goal_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = monotonic_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a  
    def peer_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = monotonic_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a
    def top_10_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = monotonic_annotate(self.a,self.s13,measure_data2,comparator_bnode)
    
    def top_25_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.a,self.s13=self.insert_annotate(self.input_graph)
        a = monotonic_annotate(self.a,self.s13,measure_data2,comparator_bnode)
        return a





        
        




