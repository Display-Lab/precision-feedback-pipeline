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
import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level='TRACE', format="<b><level>{level}</></> \t{message}")

warnings.filterwarnings("ignore")

start_time = time.time()
class Esteemer():
    def __init__(self, performer_graph, measure_list, preferences, history, mpm_df):
        # Empty dicts, lists, arrays
        self.acceptable_by_candidates=[]
        self.candidate_moderator_dict={}
        self.measure_gap_list=[]
        self.measure_gap_list_new=[]
        self.measure_trend_list=[]
        self.measure_trend_list_new=[]
        self.measure_achievement_list=[]        
        self.measure_achievement_list_new=[]   
        self.measure_loss_list=[]
        self.measure_loss_list_new=[]
        self.gap_dicts={}
        self.trend_slopes={}
        self.losses={}
        self.achievements={}    
        self.gap_dict={}
        self.trend_dict={}
        self.achievement_dict={}   
        self.loss_dict={}
        self.message_recency={}
        self.message_received_count={}
        self.measure_recency={}
        self.preferences={}
        self.df_final= pd.DataFrame()
        self.score_dict_df=pd.DataFrame()
        self.score_dict={}
        self.comp_node_dict={}


        # External objects being written to self
        self.performer_graph=performer_graph
        self.preferences=preferences
        self.history=history
        self.mpm_df=mpm_df
        self.measure_list=measure_list
        
       
       
        for s,p,o in self.performer_graph.triples( (URIRef("http://example.com/app#display-lab"), URIRef("http://example.com/slowmo#HasCandidate"), None) ):
            s1 = o   
            for s,p,o in self.performer_graph.triples((s1, URIRef("slowmo:acceptable_by"), None)):
                self.acceptable_by_candidates.append(s)
                for s2,p2,o2 in self.performer_graph.triples((s1,URIRef("slowmo:moderator"),None)):
                    self.candidate_moderator_dict[s]=o2
               
                
        logger.trace('Esteemer initialized')
        logger.debug(f'MPM DF is:\n{mpm_df}')
        logger.debug(f'Measure_list is:\n{measure_list}')
      

    ## Obtain moderators from performer graph
    def process_spek(self):
        loss=[]
        acheivement=[]
        gaps=[]
        trend_slope=[]
        self.measure_acheivement_list=[]
        Measure =None
        for x in self.measure_list:
            Measure =x
            for ss,ps,os in self.performer_graph.triples((BNode("p1"),URIRef("http://purl.obolibrary.org/obo/RO_0000091"),None)):
                s6=os
                for s123,p123,o123 in self.performer_graph.triples((s6,URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),None)):
                    #get gap sizes
                    if o123 == URIRef("http://purl.obolibrary.org/obo/PSDO_0000105") or o123 == URIRef("http://purl.obolibrary.org/obo/PSDO_0000104"):
                        for s124,p124,o124 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingMeasure"),None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                gaps.clear()
                                for s1234,p1234,o1234 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                    for s125,p125,o125 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#PerformanceGapSize"),None)):
                                        gaps.append(str(o1234))
                                        gaps.append(Measure)

                                        gaps.append(float(abs(o125)))
                                        gaps.append(float(o125))
                                        gaps_tuples=tuple(gaps)
                                        self.measure_gap_list.append(gaps_tuples)
                    #get trend slopes
                    if o123 == URIRef("http://purl.obolibrary.org/obo/PSDO_0000099") or o123 ==URIRef("http://purl.obolibrary.org/obo/PSDO_0000100"):
                        for s124,p124,o124 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingMeasure"),None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                trend_slope.clear() 
                                for s1234,p1234,o1234 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                    for s125,p125,o125 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#PerformanceTrendSlope"),None)):
                                        
                                        trend_slope.append(str(o1234))
                                        trend_slope.append(Measure)
                                        trend_slope.append(float(abs(o125)))
                                        trend_slope.append(float(o125))
                                        trend_tuples=tuple(trend_slope)
                                        self.measure_trend_list.append(trend_tuples)
                    #get number of months since last loss
                    if o123 == URIRef("http://purl.obolibrary.org/obo/PSDO_0000112") :
                        for s124,p124,o124 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingMeasure"),None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                acheivement.clear() 
                                # print(Measure)
                                for s1234,p1234,o1234 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                    for s125,p125,o125 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#TimeSinceLastAcheivement"),None)):
                                        # print(str(o1234))
                                        acheivement.append(str(o1234))
                                        acheivement.append(Measure)
                                        acheivement.append(float(o125))
                                        acheivement_tuples=tuple(acheivement)
                                        self.measure_acheivement_list.append(acheivement_tuples)
                    #get number of months since last loss
                    if o123 == URIRef("http://purl.obolibrary.org/obo/PSDO_0000113") :
                        for s124,p124,o124 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingMeasure"),None)):
                            o124=str(o124)
                            if o124 ==Measure:
                                loss.clear() 
                                for s1234,p1234,o1234 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                    for s125,p125,o125 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#TimeSinceLastLoss"),None)):
                                        # print(str(o125))
                                        loss.append(str(o1234))
                                        loss.append(Measure)
                                        loss.append(float(o125))
                                        loss_tuples=tuple(loss)
                                        self.measure_loss_list.append(loss_tuples)
        #consolidate loss moderator
        self.measure_loss_list = list(set(self.measure_loss_list))
        for x in self.measure_loss_list:
            x=list(x)
            self.measure_loss_list_new.append(x)
        #consolidate achievement moderator
        self.measure_achievement_list = list(set(self.measure_achievement_list))
        for x in self.measure_achievement_list:
            x=list(x)
        #consolidate trend moderator    
        self.measure_trend_list = list(set(self.measure_trend_list))
        for x in self.measure_trend_list:
            x=list(x)
            self.measure_trend_list_new.append(x)
        # print(*self.measure_trend_list_new)
        #consolidate gap moderator                
        self.measure_gap_list = list(set(self.measure_gap_list))
        for x in self.measure_gap_list:
            x=list(x)
            self.measure_gap_list_new.append(x)
                               
                           

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




    # Obtain MPM values    
    def process_mpm(self):
        # for col in self.mpm_df:
        #     print(col)
        self.gap_dict = dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Comparison_size))
        # for k,v in self.gap_dict.items():print(k, v)
        self.trend_dict = dict(zip(self.mpm_df.Causal_pathway, self.mpm_df.Trend_slope))
        # for k,v in self.trend_dict.items():print(k, v)
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
        a_new=[]
        score_dict={}
        # comp_node_dict={}
        df_final = pd.DataFrame()
        candidate_list=[]
        for i in self.acceptable_by_candidates:
            a_full_list=[]
            a_full_list1=[]
            b_full_list=[]
            b_full_list1=[]
            s = i
            for s5,p5,o5 in self.performer_graph.triples((s,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),None)):
                for s2we,p2we,o2we in self.performer_graph.triples((s,URIRef("slowmo:acceptable_by"),None)):
                    o2we=str(o2we)
                    accept_path=o2we
                    if "Gain" in str(o2we):
                        o2we= "Achievement"
                    if "better" in str(o2we):
                        o2we="Better"
                    if "Worse" == str(o2we):
                        o2we="Worse"
                    if "loss" in str(o2we):
                        o2we="Loss"
                    if "Approach" in str(o2we):
                        o2we="Approach"
                    s6=o5
                    for s7,p7,o7 in self.performer_graph.triples((s6,URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),None)):
                        #gap_multiplication
                        if o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000105") or o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000104"):
                            for s7,p7,o7 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):

                                a=[item for item in self.measure_gap_list_new if str(o7) in item]
                               
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
                                            j[3]=j[3]*v
                                a_full_list.append(a)
                                a_new=a[:]
                                a_new.append(accept_path)
                                a_full_list1.append(a_new)
                                
                        #trend multiplication
                        if o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000099") or o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000100"):    
                            for s8,p8,o8 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                b=[item for item in self.measure_trend_list_new if str(o8) in item]
                                
                                for k,v in self.trend_dict.items():
                                    if k == o2we:
                                        for j in b:
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            abs_val=abs(j[3])
                                            # print(abs_val)
                                            
                                            if j[2] !=abs_val:
                                                j[2]=abs_val
                                            j[2]=j[2]*v
                                            j[3]=j[3]*v
                                
                                            
                                b_full_list.append(b)
                                b_new=b[:]
                                b_new.append(accept_path)
                                b_full_list1.append(b_new)
                                # print(*b_new)
                        
                        if o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000112"):
                            for s9,p9,o9 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                c=[item for item in self.measure_achievement_list_new if str(o9) in item]
                                for k,v in self.achievement_dict.items():
                                   if k == o2we:
                                        for j in c:
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            j[2]=j[2]*v
                                c.append(i)
                                
                        if o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000113"):
                            for s10,p10,o10 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                d=[item for item in self.measure_loss_list_new if str(o10) in item]
                                for k,v in self.loss_dict.items():
                                    if k == o2we:
                                       for j in d:
                                            if v == "--":
                                                v=0
                                            v= float(v)
                                            j[2]=j[2]*v
                                d.append(i)
                                
            flat_list = [item for sublist in a_full_list1 for item in sublist]
            flat_list1=[]
            flatlist2=[]
            # print(*b_full_list1)
            if b_full_list1:
                flat_list3 = [item for sublist in b_full_list1 for item in sublist]
                flat_list4=[]
                flatlist5=[]
           
            for x in flat_list:
                if type(x) == list:
                    flat_list1=x[:]
                else:
                    flat_list1.append(x)
                flatlist2.append(flat_list1)
            # print(flat_list3)
            if b_full_list1:
                for x in flat_list3:
                    if type(x) == list:
                        flat_list4=x[:]
                    else:
                        flat_list4.append(x)
                    flatlist5.append(flat_list4)

            res = []
            [res.append(x) for x in flatlist2 if x not in res]
            res1=[res[:]]
            
            df_a = pd.DataFrame(res1, columns=['Gaps'])
            df_a_new=pd.DataFrame(df_a["Gaps"].to_list(), columns=['comp_node', 'Measure','Gaps','signed_Gaps','accept_path'])
            if b_full_list1:
                res2 = []
                [res2.append(x) for x in flatlist5 if x not in res2]
                res3=[res2[:]]
            if b_full_list1:
                df_b =pd.DataFrame(res3,columns=['Trends'])
                df_b_new =pd.DataFrame(df_b["Trends"].to_list(),columns=['comp_node','Measure','Trends','signed_trends','accept_path'])
            if (Literal('gap size'))and not(Literal('trend slope')) in self.candidate_moderator_dict[i]:
                df_merged=df_a_new
                # df_merged["gap_score"]=df_merged['Gaps']
                df_merged["score"] = df_merged['Gaps']
            if (Literal('trend slope'))and not(Literal('gap size')) in self.candidate_moderator_dict[i]:
                df_merged=df_b_new
                df_merged["score"] = df_merged['Trends'] 
            if (Literal('trend slope'))and (Literal('gap size')) in self.candidate_moderator_dict[i]:
                if not b_full_list1:
                    df_merged=df_a_new
                    # df_merged["gap_score"]=df_merged['Gaps']
                    df_merged["score"] = df_merged['Gaps']
                else:
                    df_merged=pd.merge(df_a_new, df_b_new, on='comp_node')
                    df_merged["score"] = df_merged['Gaps'] + df_merged['Trends']
            
            # gap_score_list= df_merged['gap_score']
            # print(df_b_new)
            score_list = df_merged['score'].tolist()
            comp_node_list=df_merged["comp_node"].tolist()
            candidate_list.append(i)
            
            self.score_dict[i]=score_list
            
            self.performer_graph.add((i, URIRef('http://example.com/slowmo#Score'), Literal(score_list[0])))

            self.comp_node_dict[i]=comp_node_list
            
            self.df_final = self.df_final.append(df_merged, ignore_index = True)
            
       
        #calculate gap max
        self.df_final['candidate_id']=candidate_list
        final_list=[]
        gap_df=self.df_final[self.df_final[['Gaps']].notnull().all(1)]
        gap_df = gap_df[['candidate_id', 'score']]
        index = gap_df.nlargest(1, 'score')
        gapmax=index['candidate_id'][1]
        final_list.append(gapmax)
        #calculate trend max
        trend_df=self.df_final[(self.df_final[['Gaps']].isna().all(1))]
        trend_df = trend_df[['candidate_id', 'score']]
        trend_df = trend_df.reset_index()
        index = trend_df.nlargest(1,'score')
        trendmax=index['candidate_id'][1]
        final_list.append(trendmax)
        #choose random node between gapmax and trendmax
        Keymax=random.choice(final_list)
        # Keymax = max(zip(self.score_dict.values(), self.score_dict.keys()))[1]
        logger.debug(f'DF_Final is:\n{self.df_final}') 
        self.node=Keymax
        return self.node,self.performer_graph,self.df_final,self.score_dict_df,self.comp_node_dict

    
   

    #get selected message   
    def get_selected_message(self):
        s_m={}
        a=0
        # print(self.node)
        if self.node== "No message selected":
            s_m["message_text"]="No message selected"
            return s_m 
        else:
            s=self.node
            temp_name = URIRef("http://example.com/slowmo#name")   # URI of template name?
            p232= URIRef("psdo:PerformanceSummaryDisplay")
            Display=["text only", "bar chart", "line graph"]
            comparator_types=["Top 25","Top 10","Peers","Goal"]
            sw=0
            o2wea=[]
            
            
            ## Format selected_candidate to return for pictoralist-ing
            for s21,p21,o21 in self.performer_graph.triples((s,URIRef("http://example.com/slowmo#AncestorTemplate"),None)):
                s_m["template_id"] = o21
            # Duplicate logic above and use to pull template name
            for s21,p21,o21 in self.performer_graph.triples((s,temp_name,None)):
                s_m["template_name"] = o21
            
            for s2,p2,o2 in self.performer_graph.triples((s,URIRef("psdo:PerformanceSummaryTextualEntity"),None)):
                s_m["message_text"] = o2
            # for s212,p212,o212 in self.spek_tp.triples((s,p232,None)):
               
            s_m["display"]=random.choice(Display)
            # for s9,p9,o9 in self.spek_tp.triples((s,p8,None)):
            #     s_m["Comparator Type"] = o9
            for s2we,p2we,o2we in self.performer_graph.triples((s,URIRef("slowmo:acceptable_by"),None)):
                o2wea.append(o2we)
            # print(*o2wea)
            s_m["acceptable_by"] = o2wea

            comparator_list=[]

            for s5,p5,o5 in self.performer_graph.triples((s,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),None)):
                s6=o5
                #print(o5)
                for s7,p7,o7 in self.performer_graph.triples((s6,URIRef("http://example.com/slowmo#RegardingMeasure"),None)):
                    s_m["measure_name"]=o7
                    s10= BNode(o7)
                    for s11,p11,o11 in self.performer_graph.triples((s10, URIRef("http://purl.org/dc/terms/title"),None)):
                        s_m["measure_title"]=o11
                for s14,p14,o14 in self.performer_graph.triples((s6,RDF.type,None)):
                    #print(o14)
                    if o14==URIRef("http://purl.obolibrary.org/obo/PSDO_0000128"):
                        comparator_list.append("Top 25")
                        # s_m["comparator_type"]="Top 25"                        
                    if o14==URIRef("http://purl.obolibrary.org/obo/PSDO_0000129"):
                        comparator_list.append("Top 10")
                        # s_m["comparator_type"]="Top 10"
                    if o14==URIRef("http://purl.obolibrary.org/obo/PSDO_0000126"):
                        comparator_list.append("Peers")
                        # s_m["comparator_type"]="Peers"
                    if o14==URIRef("http://purl.obolibrary.org/obo/PSDO_0000094"):
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