import warnings
import time
import logging
import random
import io
import pandas as pd
#from asyncore import read
from io import StringIO
from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF
from decimal import *
import numpy as np
#from process_history import retrieve_history_data, rank_history_component  # Having issues with this...
import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level='TRACE', format="<b><level>{level}</></> \t{message}")




# from .load_for_real import load
# from load import read, transform,read_contenders,read_measures,read_comparators
# from score import score, select,apply_indv_preferences,apply_history_message

# load()

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
# Read graph and convert to dataframe
start_time = time.time()
class Esteemer():
    def __init__(self, spek_tp, measure_list, preferences, history, mpm_df):
        # Empty dicts, lists, arrays
        self.y=[]
        self.measure_gap_list=[]
        self.measure_gap_list_new=[]
        self.measure_trend_list=[]
        self.measure_trend_list_new=[]
        self.measure_acheivement_list=[]        # spelling
        self.measure_acheivement_list_new=[]    # spelling
        self.measure_loss_list=[]
        self.measure_loss_list_new=[]
        self.gap_dicts={}
        self.trend_slopes={}
        self.losses={}
        self.acheivements={}    # spelling
        self.gap_dict={}
        self.trend_dict={}
        self.acheivement_dict={}    # spelling
        self.loss_dict={}
        self.message_recency={}
        self.message_received_count={}
        self.measure_recency={}
        self.preferences={}

        # External objects being written to self
        self.spek_tp=spek_tp
        self.preferences=preferences
        self.history=history
        self.mpm_df=mpm_df
        self.measure_list=measure_list
        
        # New variables (none are currently required?)
        self.display_lab_app_uri=URIRef("http://example.com/app#display-lab")       # one ref
        self.slowmo_has_candidate=URIRef("http://example.com/slowmo#HasCandidate")  # one ref
        self.slowmo_acceptable_by=URIRef("slowmo:acceptable_by")                    # one ref
        self.slowmo_score=URIRef('http://example.com/slowmo#Score')                 # one ref
        #self.o2=Literal(1)     # Replace with direct reference, just one usage
        
        ## 
        for s,p,o in self.spek_tp.triples( (self.display_lab_app_uri, self.slowmo_has_candidate, None) ):
            s1 = o   #?
            for s,p,o in self.spek_tp.triples((s1, self.slowmo_acceptable_by, None)):
                self.spek_tp.add((s, self.slowmo_score, Literal(1)))
                self.y.append(s)
                
        logger.trace('Esteemer initialized')
        logger.debug(f'MPM DF is:\n{mpm_df}')
        logger.debug(f'Measure_list is:\n{measure_list}')
        #logger.debug(f'Var "s" adds to dict "y", forming y as:\n{self.y}')


    ## Process annotations from thinkpudding
    def process_spek(self):
        # print(*self.y)
        sh=BNode("p1")
        ph=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
        p4=URIRef("http://example.com/slowmo#RegardingMeasure")
        p5=URIRef("http://example.com/slowmo#RegardingComparator")
        ph33=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        ph3=URIRef("http://purl.obolibrary.org/obo/PSDO_0000099")
        ph4=URIRef("http://purl.obolibrary.org/obo/PSDO_0000100")
        ph5=URIRef("http://purl.obolibrary.org/obo/PSDO_0000105")
        ph6=URIRef("http://purl.obolibrary.org/obo/PSDO_0000104")
        ph7=URIRef("http://purl.obolibrary.org/obo/PSDO_0000113")
        ph8=URIRef("http://purl.obolibrary.org/obo/PSDO_0000112")
        ph9=URIRef("http://example.com/slowmo#PerformanceGapSize")
        ph10=URIRef("http://example.com/slowmo#PerformanceTrendSlope")
        ph11=URIRef("http://example.com/slowmo#TimeSinceLastLoss")
        ph12=URIRef("http://example.com/slowmo#TimeSinceLastAcheivement")

        loss=[]
        acheivement=[]
        gaps=[]
        trend_slope=[]

        self.measure_gap_list=[]
        self.measure_trend_list=[]
        self.measure_acheivement_list=[]
        self.measure_loss_list=[]
        
        Measure =None

        ## Iterate through measures, add annotations to new lists (why?)
        for x in self.measure_list:
            Measure =x
            for ss,ps,os in self.spek_tp.triples((sh,ph,None)):
                s6=os
                for s123,p123,o123 in self.spek_tp.triples((s6,ph33,None)):
                    if o123 == ph5 or o123 == ph6:
                        for s124,p124,o124 in self.spek_tp.triples((s6,p4,None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                gaps.clear()
                                for s1234,p1234,o1234 in self.spek_tp.triples((s6,p5,None)):
                                    for s125,p125,o125 in self.spek_tp.triples((s6,ph9,None)):
                                        gaps.append(str(o1234))
                                        gaps.append(Measure)

                                        gaps.append(float(abs(o125)))
                                        gaps.append(float(o125))
                                        gaps_tuples=tuple(gaps)
                                        self.measure_gap_list.append(gaps_tuples)
                    if o123 == ph3 or o123 ==ph4:
                        for s124,p124,o124 in self.spek_tp.triples((s6,p4,None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                trend_slope.clear() 
                                for s1234,p1234,o1234 in self.spek_tp.triples((s6,p5,None)):
                                    for s125,p125,o125 in self.spek_tp.triples((s6,ph10,None)):
                                        
                                        trend_slope.append(str(o1234))
                                        trend_slope.append(Measure)
                                        trend_slope.append(float(o125))
                                        trend_tuples=tuple(trend_slope)
                                        self.measure_trend_list.append(trend_tuples)
                    if o123 == ph8 :
                        for s124,p124,o124 in self.spek_tp.triples((s6,p4,None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                acheivement.clear() 
                                # print(Measure)
                                for s1234,p1234,o1234 in self.spek_tp.triples((s6,p5,None)):
                                    for s125,p125,o125 in self.spek_tp.triples((s6,ph12,None)):
                                        # print(str(o1234))
                                        acheivement.append(str(o1234))
                                        acheivement.append(Measure)
                                        acheivement.append(float(o125))
                                        acheivement_tuples=tuple(acheivement)
                                        self.measure_acheivement_list.append(acheivement_tuples)
                    
                    if o123 == ph7 :
                        for s124,p124,o124 in self.spek_tp.triples((s6,p4,None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                loss.clear() 
                                for s1234,p1234,o1234 in self.spek_tp.triples((s6,p5,None)):
                                    for s125,p125,o125 in self.spek_tp.triples((s6,ph11,None)):
                                        # print(str(o125))
                                        loss.append(str(o1234))
                                        loss.append(Measure)
                                        loss.append(float(o125))
                                        loss_tuples=tuple(loss)
                                        self.measure_loss_list.append(loss_tuples)
        self.measure_loss_list = list(set(self.measure_loss_list))
        for x in self.measure_loss_list:
            x=list(x)
            self.measure_loss_list_new.append(x)
        # print(*self.measure_loss_list_new)
        # print(*self.measure_loss_list)
        self.measure_acheivement_list = list(set(self.measure_acheivement_list))
        for x in self.measure_acheivement_list:
            x=list(x)
            # self.measure_acheivement_list_new.append(x)
        # print(*self.measure_acheivement_list_new)
        # print(*self.measure_acheivement_list) 
        self.measure_trend_list = list(set(self.measure_trend_list))
        for x in self.measure_trend_list:
            x=list(x)
            self.measure_trend_list_new.append(x)
        # print(*self.measure_trend_list_new)                 
        self.measure_gap_list = list(set(self.measure_gap_list))
        for x in self.measure_gap_list:
            x=list(x)
            self.measure_gap_list_new.append(x)
        print(*self.measure_gap_list_new)                        
                           

    ## Pull in history component of input message from dict to dataframe for calculations:
    def process_history(self):
        logger.trace('Running esteemer.retrieve_history_data...')
        # Define blank output matrix as a list of dictionaries
        history_component_matrix = []


        # Iterate through items in 'History'
        for month, data in self.history.items():
            if data:  # Check if the month has data

                # Create a dictionary for each row in the output matrix per month in history
                output_matrix_row = {
                    'Month': month,
                    'Measure': data.get('measure', ''),
                    'Template Name': data.get('message_template_name', ''),
                    'Message Instance ID': data.get('message_instance_id', ''),
                    'Message datetime': data.get('message_generated_datetime', ''),
                }
                # Append the row to the output matrix
                history_component_matrix.append(output_matrix_row)

        # Convert the list of dictionaries to a pandas DataFrame
        outcome_matrix = pd.DataFrame(history_component_matrix)

        # Print the DataFrame (optional, for debugging)
        logger.debug(f'History matrix is\n{outcome_matrix}')

        return outcome_matrix



    ## Determine values for history components (measure recency, message recency):
    def rank_history_component(self, history_matrix, acceptable_candidates):
        logger.trace('Running esteemer.rank_history_component...')
        # where history_matrix = retrieve_history_data(acceptable_candidate)

        # 1) Assign time 0 (current feedback month) | Once MPOG generating 'current_month', pull through from spek instead of latest month in dataframe...
        this_month = pd.to_datetime(latest_month = history_matrix['Month'].idxmax())    #acceptable_candidate['current_month']) # Trace back acceptable candidate in spek_tp, pull key through to spek

        # 2) Define dicts for data output
        message_recency_dict = {}
        measure_recency_dict = {}
        

        # 3) Compare row 'month' to t0, convert to integers representing time in months between extant feedback and current month
        history_matrix['Time_Since_t0'] = (
            pd.to_datetime(history_matrix['Month']) - this_month
        ).astype('<m8[M]').astype(int)

        # 4) Calculate message recency
        for candidate in acceptable_candidates:

            # Filter matrix for the specific candidate
            candidate_rows = history_matrix[
                (history_matrix['message_template_name'] == candidate['message_template_name']) &
                (history_matrix['Measure'] == candidate['measure'])
            ]

            # Calculate months since last occurrence of same message
            if not candidate_rows.empty:
                last_occurrence = candidate_rows['Distance_From_t0'].max()
                message_recency_dict[candidate['message_template_name']] = last_occurrence
            else:
                message_recency_dict[candidate['message_template_name']] = None

        # 5) Calculate measure recency
        for candidate in acceptable_candidates:
            candidate_measure = candidate['measure']

            # Filter matrix for the specific candidate measure
            candidate_rows = history_matrix[history_matrix['Measure'] == candidate_measure]

            # Calculate months since last occurrence of same measure
            if not candidate_rows.empty:
                last_occurrence = candidate_rows['Distance_From_t0'].max()
                measure_recency_dict[candidate['measure']] = last_occurrence
            else:
                measure_recency_dict[candidate['measure']] = None

        # Print the recency dictionaries
        logger.debug("Message Recency:", message_recency_dict)
        logger.debug("Measure Recency:", measure_recency_dict)
        
        self.message_recency_dict = message_recency_dict
        self.measure_recency_dict = measure_recency_dict




    ### Process MPM dict    
    def process_mpm(self):
        # for col in self.mpm_df:
        #     print(col)
        self.gap_dict = dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Comparison_size))
        # for k,v in self.gap_dict.items():print(k, v)
        self.trend_dict = dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Trend_slope))
        # for k,v in self.gap_dict.items():print(k, v)
        self.acheivement_dict = dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Measure_achievement_recency))
        # for k,v in self.acheivement_dict.items():print(k, v)
        self.loss_dict=dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Loss_recency))
        # for k,v in self.loss_dict.items():print(k, v)
        self.message_recency=dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Message_recency))
        # for k,v in self.message_recency.items():print(k, v)
        self.measure_recency=dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Measure_recency))
        # for k,v in self.measure_recency.items():print(k, v)
    

    ### Score candidates individually
    def score(self):
        # print(*self.measure_gap_list) 
        j_new=()
        a_new=[]
        score_dict={}
        comp_node_dict={}
        df_final = pd.DataFrame()
        # print("acceptable by")
        # print(*self.y)
        ## Makes candidate list, iterates through candidates
        for i in self.y:
            a_full_list=[]
            a_full_list1=[]
            b_full_list=[]
            
            # print(i)
            s = i
            pwed = URIRef("slowmo:acceptable_by")
            p3=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
            ph33=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
            ph5=URIRef("http://purl.obolibrary.org/obo/PSDO_0000105")
            ph6=URIRef("http://purl.obolibrary.org/obo/PSDO_0000104")
            ph3=URIRef("http://purl.obolibrary.org/obo/PSDO_0000099")
            ph4=URIRef("http://purl.obolibrary.org/obo/PSDO_0000100")
            p4=URIRef("http://example.com/slowmo#RegardingComparator")
            ph7=URIRef("http://purl.obolibrary.org/obo/PSDO_0000113")
            ph8=URIRef("http://purl.obolibrary.org/obo/PSDO_0000112")

            # for s2we,p2we,o2we in self.spek_tp.triples((s,pwed,None)):
            #     print(o2we)
                # o2wea.append(o2we)
            for s5,p5,o5 in self.spek_tp.triples((s,p3,None)):
                for s2we,p2we,o2we in self.spek_tp.triples((s,pwed,None)):
                    o2we=str(o2we)
                    accept_path=o2we
                    if "Gain" in str(o2we):
                        o2we= "Achievement"
                    if "better" in str(o2we):
                        o2we="Better"
                    if "Worse" in str(o2we):
                        o2we="Worse"
                    if "loss" in str(o2we):
                        o2we="Loss"
                    if "Approach" in str(o2we):
                        o2we="Approach"
                    # print(o5)
                    
                    s6=o5
                    # for s8,p8,o8 in self.spek_tp.triples((s6,p5,None)):
                    #             print(s6)
                    for s7,p7,o7 in self.spek_tp.triples((s6,ph33,None)):
                        #gap_multiplication
                        if o7==ph5 or o7==ph6:
                            for s7,p7,o7 in self.spek_tp.triples((s6,p4,None)):

                                a=[item for item in self.measure_gap_list_new if str(o7) in item]
                                # a_new = a
                                # a_new.append(accept_path)
                                
                                # print("cal")
                                for k,v in self.gap_dict.items():
                                    if k == o2we:
                                        for j in a:
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            abs_val=abs(j[3])
                                            if j[2] !=abs_val:
                                                j[2]=abs_val
                                            j[2]=j[2]*v
                                # a.append(i)
                                # a_new.append(accept_path)
                                # a.append(accept_path)
                                a_full_list.append(a)

                                a_new=a[:]
                                a_new.append(accept_path)
                                a_full_list1.append(a_new)
                                # print(*a_new)
                                # a_new.append(accept_path)
                                # print(*a_new)
                                # print(accept_path)
                                # print(*a)
                            # print(*a_full_list)
                            # print("\n")
                                # df_a= pd.DataFrame(a, columns = ['measure', 'node'])
                                # print(df_a)
                                # print("\n")
                                # size = len(a)
                                # print(size)
                        #     a_full_list.append(a)
                        # a_full_list = list(set(a_full_list))
                        # print(*a_full_list)
                        # print(len(a_full_list))
                        #trend multiplication
                        if o7==ph3 or o7==ph4:    
                            for s8,p8,o8 in self.spek_tp.triples((s6,p4,None)):
                                b=[item for item in self.measure_trend_list_new if str(o8) in item]
                                # print(*b)
                                # print("before")
                                for k,v in self.trend_dict.items():
                                    if k == o2we:
                                        for j in b:
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            
                                            j[2]=j[2]*v
                                            # j.append(i)
                                # b.append(i)
                                b_full_list.append(b)
                                # print(*b)
                                # print("\n")
                        # print(o2we)
                        if o7==ph8:
                            # print(o7)
                            # print(ph7)
                            # # print(ph7)
                            # print(o2we)   
                            for s9,p9,o9 in self.spek_tp.triples((s6,p4,None)):
                                c=[item for item in self.measure_acheivement_list_new if str(o9) in item]
                                # print(*c)
                                # print("multiplication")
                                for k,v in self.acheivement_dict.items():
                                    # print(o2we)
                                    # print(k)
                                    # print(o2we)
                                    if k == o2we:
                                        # print(k)
                                        # print(o2we)
                                        # print(o2we)
                                        for j in c:
                                            # print(*j)
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            j[2]=j[2]*v
                                            # j.append(i)
                                c.append(i)
                                # print(*c)
                                # print("\n")
                        if o7==ph7:
                            # print(o2we)    
                            for s10,p10,o10 in self.spek_tp.triples((s6,p4,None)):
                                d=[item for item in self.measure_loss_list_new if str(o10) in item]
                                # print(*d)
                                for k,v in self.loss_dict.items():
                                    if k == o2we:
                                        # print(k)
                                        # print(o2we)
                                        # print(o2we)
                                        for j in d:
                                            # print(*j)
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            j[2]=j[2]*v
                                            # j.append(i)
                                d.append(i)
                                # print(*d)
                                # print("\n")
                                # print(*d)
                       
            # print("outer loop")
            # print(*a_full_list)
            # print(*a_full_list1)
            flat_list = [item for sublist in a_full_list1 for item in sublist]
            flat_list1=[]
            flatlist2=[]
            # print(*flat_list)
            # flat_list1 = [item for sublist in flat_list for item in sublist]
            for x in flat_list:
                if type(x) == list:
                    flat_list1=x[:]
                else:
                    flat_list1.append(x)
                flatlist2.append(flat_list1)
            res = []
            [res.append(x) for x in flatlist2 if x not in res]
            res1=[res[:]]
            # print(*res1)
            # print(*flatlist2)
            # print(*a_full_list)
            df_a = pd.DataFrame(res1, columns=['Gaps'])
            # print(df_a.loc[[0]])
            # print(df_a)
            df_b =pd.DataFrame(b_full_list,columns=['Trends'])
            # print(df_b)
            df_a_new=pd.DataFrame(df_a["Gaps"].to_list(), columns=['comp_node', 'Measure','Gaps','signed_Gaps','accept_path'])
            # df_a_new=pd.DataFrame(df_a["accept_path"].to_list(), columns=['comp_node', 'Measure','Gaps','signed_Gaps','accept_path'])
            df_b_new =pd.DataFrame(df_b["Trends"].to_list(),columns=['comp_node','Measure','Trends'])
            # print(df_a_new.loc[[0]])
            # print(df_b_new)
            if df_b_new.empty:
                df_merged=df_a_new
                df_merged["score"] = df_merged['Gaps']
            else:
                df_merged=pd.merge(df_a_new, df_b_new, on='comp_node')
                df_merged["score"] = df_merged['Gaps'] + df_merged['Trends'] 
            score_list = df_merged['score'].tolist()
            comp_node_list=df_merged["comp_node"].tolist()

            # score_max = max(score_list)
            # print(score_max)
            score_dict[i]=score_list
            comp_node_dict[i]=comp_node_list
            # print(i)
            # print(score_list)
            df_final = df_final.append(df_merged, ignore_index = True)
            logger.debug(f'DF_Final is:\n{df_final}')   # Inside loop over spo 5, spo5 represents candidates? Doesn't seem to be the case...
            #logger.debug(f'\nS5:\n{s5}\n\nP5:\n{p5}\no5:\n{o5}\n')
            logger.debug(f'df_merged is:\n{df_merged}')
            # print("\n")
        
        
        Keymax = max(zip(score_dict.values(), score_dict.keys()))[1]
        # Valuemax= max(zip(score_dict.values(), score_dict.keys()))[0]

        for k2,v2 in score_dict.items():
            print(k2,v2)
        
        index_list=[]
        df_final1=df_final.iloc[df_final.score.argmax()]
        print(df_final1)
        if df_final1['accept_path']=="Social better":
            
            rslt_df = df_final.loc[df_final['accept_path'] == "Social better"]
            if "Measure" not in rslt_df.columns:
                rslt_df["Measure"]=np.nan
            if "Measure_x" not in rslt_df.columns:
                rslt_df["Measure_x"]=np.nan
            if "Measure_y" not in rslt_df.columns:
                rslt_df["Measure_y"]=np.nan
            cols = ['Measure', 'Measure_y']
            rslt_df["Measures"] = [[e for e in row if e==e] for row in rslt_df[cols].values]
            rslt_df = rslt_df.drop('Measure', axis=1)
            rslt_df = rslt_df.drop('Measure_x', axis=1)
            rslt_df = rslt_df.drop('Measure_y', axis=1)
            rslt_df ['Measures1'] = [','.join(map(str, l)) for l in rslt_df['Measures']]
           
            if (rslt_df['signed_Gaps'] > 0).all():
                # print("yes")
                result=rslt_df.groupby('accept_path')['score'].nsmallest(2).droplevel(0).iloc[0]
                
                Kew=[k for k, v in score_dict.items() if result in v]

                self.node=random.choice(Kew)
                return self.node,self.spek_tp
            if (rslt_df['signed_Gaps'] == 0.00).any():
                # print("yes")
                rsdf=rslt_df.sample(n=1)
                # print(rsdf)
                #rdf=rslt_df.loc[rslt_df['Measures'] == rsdf["Measures"].values]

                # result=rslt_df
                measure_selected=rsdf["Measures"].values[0]
                # print(type(measure_selected))
                measure_selected=" ".join(map(str,measure_selected))
                # print(type(measure_selected))
                # print(rslt_df)
                new_df = rslt_df[(rslt_df['Measures1']==measure_selected )]
                # print(new_df)
                comp_node_list = new_df['comp_node'].tolist()
                # print(*comp_node_list)
                final_x=0
                for x in comp_node_list:
                    x=BNode(x)
                    # print(x)
                    # print(type(x))
                    p5=URIRef("http://example.com/slowmo#RegardingComparator")
                    p22=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
                    top_10=URIRef("http://purl.obolibrary.org/obo/PSDO_0000129")
                    for s1234,p1234,o1234 in self.spek_tp.triples((None,p5,x)):
                        for sa,pa,oa in self.spek_tp.triples((s1234,p22, None)):
                            if oa == top_10:
                                final_x= x
                # print(final_x)
                
                if final_x == 0:
                    final_x= random.choice(comp_node_list)
                else:
                    final_x=str(final_x)            
                Kew1=[k for k, v in comp_node_dict.items() if final_x in v]
                # print(*Kew1)
                self.node=Kew1[0]
                return self.node,self.spek_tp 
                        

            
        self.node=Keymax
            
        return self.node,self.spek_tp
        # for k,v in score_dict.items():print(k, v)
    # # def select(self):
    #     self.scores=[]
    #     nodes=[]
    #     # print(*self.y)
    #     if len(self.y)!=0:
    #         self.node=random.choice(self.y)
    #     else:
    #         self.node="No message selected"

    #     if self.node== "No message selected":
    #         return self.node,self.spek_tp
    #     else:
    #         o2=URIRef("http://example.com/slowmo#selected")
    #         self.spek_tp.add((self.node,RDF.type,o2))
    #         return self.node,self.spek_tp

    def get_selected_message(self):
        s_m={}
        a=0
        # print(self.node)
        if self.node== "No message selected":
            s_m["message_text"]="No message selected"
            return s_m 
        else:
            s=self.node
            p1=URIRef("psdo:PerformanceSummaryTextualEntity")
            pwed=URIRef("slowmo:acceptable_by")
            p3=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
            p4=URIRef("http://example.com/slowmo#RegardingMeasure")
            p8=URIRef("http://example.com/slowmo#name")
            p10= URIRef("http://purl.org/dc/terms/title")
            p12=URIRef("http://purl.obolibrary.org/obo/PSDO_0000128")
            p13=URIRef("http://purl.obolibrary.org/obo/PSDO_0000129")
            p14=URIRef("http://purl.obolibrary.org/obo/PSDO_0000126")
            p15=URIRef("http://purl.obolibrary.org/obo/PSDO_0000094")
            p20=URIRef("http://example.com/slowmo#AncestorTemplate")
            pqd=URIRef("http://example.com/slowmo#PerformanceGapSize")
            pqw=URIRef("http://example.com/slowmo#PerformanceTrendSlope")
            
            temp_name = URIRef("http://example.com/slowmo#name")   # URI of template name?
            
            p232= URIRef("psdo:PerformanceSummaryDisplay")
            Display=["text only", "bar chart", "line graph"]
            comparator_types=["Top 25","Top 10","Peers","Goal"]
            sw=0
            o2wea=[]
            # spek_out_dicts={}
            # s=URIRef("http://example.com/app#display-lab")
            # p=URIRef("http://example.com/slowmo#HasCandidate")
            # p1=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
            # i=0
            # a=[]
            # for s,p,o in spek_tp.triples( (s, p, None) ):
            #     s1= o
            #     y=[o for s,p,o in spek_tp.triples((s1,p1,None))]
            #     # print(*y)
            #     for i in range(len(y)):
            #         s=y[i]
            #         for s,p,o in spek_cs.triples((s,RDF.type,None)):
            #             a.append(o)
            #             y[i]=o
            #     spek_out_dicts[s1] = y
            
            ## Format selected_candidate to return for pictoralist-ing
            for s21,p21,o21 in self.spek_tp.triples((s,p20,None)):
                s_m["template_id"] = o21
            # Duplicate logic above and use to pull template name
            for s21,p21,o21 in self.spek_tp.triples((s,temp_name,None)):
                s_m["template_name"] = o21
            
            for s2,p2,o2 in self.spek_tp.triples((s,p1,None)):
                s_m["message_text"] = o2
            # for s212,p212,o212 in self.spek_tp.triples((s,p232,None)):
               
            s_m["display"]=random.choice(Display)
            # for s9,p9,o9 in self.spek_tp.triples((s,p8,None)):
            #     s_m["Comparator Type"] = o9
            for s2we,p2we,o2we in self.spek_tp.triples((s,pwed,None)):
                o2wea.append(o2we)
            # print(*o2wea)
            s_m["acceptable_by"] = o2wea

            
            
            

            
                
            comparator_list=[]

            for s5,p5,o5 in self.spek_tp.triples((s,p3,None)):
                s6=o5
                #print(o5)
                for s7,p7,o7 in self.spek_tp.triples((s6,p4,None)):
                    s_m["measure_name"]=o7
                    s10= BNode(o7)
                    for s11,p11,o11 in self.spek_tp.triples((s10,p10,None)):
                        s_m["measure_title"]=o11
                for s14,p14,o14 in self.spek_tp.triples((s6,RDF.type,None)):
                    #print(o14)
                    if o14==p12:
                        comparator_list.append("Top 25")
                        # s_m["comparator_type"]="Top 25"                        
                    if o14==p13:
                        comparator_list.append("Top 10")
                        # s_m["comparator_type"]="Top 10"
                    if o14==p14:
                        comparator_list.append("Peers")
                        # s_m["comparator_type"]="Peers"
                    if o14==p15:
                        comparator_list.append("Goal")
                        # s_m["comparator_type"]="Goal"
            for i in comparator_list:
                if i is not None:
                    a=i
            s_m["comparator_type"]=a            
            return s_m


    
# logging.critical("--score and select %s seconds ---" % (time.time() - start_time1))
# print(finalData)

# time_taken = time.time()-start_time
logging.debug("---Esteemer run time: %s seconds ---" % (time.time() - start_time))

"""with open('data.json', 'a') as f:
    f.write(finalData + '\n')"""