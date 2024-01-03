import warnings
 

import pandas as pd
from rdflib import Graph, URIRef, BNode
from rdflib.namespace import RDF
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
    
    def __init__(self,performer_graph:Graph,performance_data:pd.DataFrame):
        self.performance_data=performance_data
        self.data = pd.DataFrame()
        performance_rate =[]
        for rowIndex, row in self.performance_data.iterrows():
            if (row['passed_count']==0 and row['denominator']==0):
                performance_rate.append(0.0)
            else:
                performance_rate.append(row['passed_count']/row['denominator'])
        #accessing the data from the input message
        self.performance_data['Performance_Rate']=performance_rate
        self.performance_data['peer_average_comparator']=self.performance_data['peer_average_comparator']/100
        self.performance_data['peer_90th_percentile_benchmark']=self.performance_data['peer_90th_percentile_benchmark']/100
        self.performance_data['peer_75th_percentile_benchmark']=self.performance_data['peer_75th_percentile_benchmark']/100
        self.performance_data['MPOG_goal']=self.performance_data['MPOG_goal']/100
        self.performance_data['month'] = pd.to_datetime(self.performance_data['month'])
        self.performance_data[['measure']] = self.performance_data[['measure']].astype(str)
        self.performance_data.measure = self.performance_data.measure.str.encode('utf-8')
        self.data["measure"]=self.performance_data["measure"].str.decode(encoding="UTF-8")
        self.data["month"]=self.performance_data["month"].astype('datetime64')
        self.data[['peer_average_comparator']] = self.performance_data[['peer_average_comparator']].astype(float)
        self.data[['peer_90th_percentile_benchmark']] = self.performance_data[['peer_90th_percentile_benchmark']].astype(float)
        self.data[['peer_75th_percentile_benchmark']] = self.performance_data[['peer_75th_percentile_benchmark']].astype(float)
        self.data[['Performance_Rate']] = self.performance_data[['Performance_Rate']].astype(float)
        self.data[['goal_comparison_value']] = self.performance_data[['MPOG_goal']].astype(float)
        idx= self.data.groupby(['measure'])['month'].transform(max) == self.data['month']
        self.latest_measure = self.data[idx]
        self.performer_graph=performer_graph

    def prepare_data_measure_name(self,measure_name:str,**goal_dicts):
        global measure_data1
        measure_data1 = self.latest_measure[self.latest_measure['measure'] == measure_name] # measure_data1 contains record of latest timepoint
        global measure_data2
        measure_data2 = self.data[self.data['measure'] == measure_name]#it contains data with last three timepoints
        bnode=BNode(measure_name)
        global comparator_bnode
        comparator_bnode=goal_dicts.get(bnode)
        return measure_data1,measure_data2,comparator_bnode
        
    def insert_annotate(self,performer_graph):
        self.performer_graph.add((URIRef('http://example.com/app#display-lab'),URIRef('http://example.com/slowmo#IsAboutPerformer'),BNode('p1')))
        p1_node=BNode('p1')
        self.performer_graph.add((p1_node,RDF.type,URIRef("http://purl.obolibrary.org/obo/psdo_0000085")))
        return self.performer_graph,p1_node
    
    def goal_gap_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
        self.performer_graph = goal_gap_annotate(self.performer_graph,self.p1_node,measure_data1,comparator_bnode)
        return self.performer_graph

    def peer_gap_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
        self.performer_graph = peer_gap_annotate(self.performer_graph,self.p1_node,measure_data1,comparator_bnode)
        return self.performer_graph
    
    def top_10_gap_annotate(self,measure_name:str,**top_10_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**top_10_dicts)
        self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
        self.performer_graph = top_10_gap_annotate(self.performer_graph,self.p1_node,measure_data1,comparator_bnode)
        return self.performer_graph
    
    def top_25_gap_annotate(self,measure_name:str,**top_10_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**top_10_dicts)
        self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
        self.performer_graph = top_25_gap_annotate(self.performer_graph,self.p1_node,measure_data1,comparator_bnode)
        return self.performer_graph


    def goal_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = trend_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph

    def peer_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = trend_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph
    
    def top_10_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = trend_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph

    def top_25_trend_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = trend_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph
    
    
    def goal_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = goal_acheivementloss_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph

    def peer_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = peer_acheivementloss_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph  
        else:
            return self.performer_graph
        
    def top_10_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = top_10_acheivementloss_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph
        

    def top_25_acheivement_loss_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = top_25_acheivementloss_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph


    def goalconsecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = goal_consecutive_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph 
        else:
            return self.performer_graph  

    def peerconsecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = peer_consecutive_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph

    def top_10consecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = top_10_consecutive_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph 
        
    def top_25consecutive_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = top_25_consecutive_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph 
        else:
            return self.performer_graph
    def goal_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = monotonic_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph  
    def peer_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = monotonic_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph
    def top_10_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = monotonic_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph
        
    def top_25_monotonicity_annotate(self,measure_name:str,**goal_dicts):
        measure_data1,measure_data2,comparator_bnode=self.prepare_data_measure_name(measure_name,**goal_dicts)
        if measure_data2.shape[0]>3:
            self.performer_graph,self.p1_node=self.insert_annotate(self.performer_graph)
            self.performer_graph = monotonic_annotate(self.performer_graph,self.p1_node,measure_data2,comparator_bnode)
            return self.performer_graph
        else:
            return self.performer_graph




        
        




