import json
import random
import sys
import warnings
import operator

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

warnings.filterwarnings("ignore")


def score(meaningful_messages_final):
    len = meaningful_messages_final.shape[0]
    score = random.sample(range(10, 1000), len)
    meaningful_messages_final["score"] = score
    meaningful_messages_final.reset_index(drop=True, inplace=True)
    #meaningful_messages_final.to_csv("df_es1.csv")
    return meaningful_messages_final
    # meaningful_messages_final.to_csv("df_es1.csv")




def apply_indv_preferences(meaningful_messages_final,indv_preferences_read):
    indv_preferences_df = pd.json_normalize(indv_preferences_read)
    display_preferences_df =indv_preferences_df [['Utilities.Display_Format.short_sentence_with_no_chart', 'Utilities.Display_Format.bar_chart','Utilities.Display_Format.line_graph']]
    message_preferences_df =indv_preferences_df[['Utilities.Message_Format.1','Utilities.Message_Format.2','Utilities.Message_Format.16','Utilities.Message_Format.24','Utilities.Message_Format.18','Utilities.Message_Format.11','Utilities.Message_Format.22','Utilities.Message_Format.14','Utilities.Message_Format.21']]
    
    display_preferences,max_val = displaypreferences(meaningful_messages_final,display_preferences_df)
    messages_preferences= messagepreferences(display_preferences,message_preferences_df)
   
    #display_preferences_df.to_csv('display_preferences.csv')
    #message_preferences_df.to_csv('message_preferences_df.csv')
    #indv_preferences_df.to_csv('individual_preferences.csv')
    #messages_preferences.to_csv('message_preferences_final.csv')
    return messages_preferences ,max_val

def displaypreferences(meaningful_messages_final,display_preferences_df):
    nochart_pref=display_preferences_df.at[0,'Utilities.Display_Format.short_sentence_with_no_chart']
    bar_pref=display_preferences_df.at[0,'Utilities.Display_Format.bar_chart']
    line_pref=display_preferences_df.at[0,'Utilities.Display_Format.line_graph']
    line_pref = float(line_pref)
    bar_pref = float(bar_pref)
    nochart_pref = float(nochart_pref)
    my_dict = {"line_pref":[],"bar_pref":[],"nochart_pref":[]}
    if line_pref == 0:
        line_pref= 1
    elif bar_pref == 0:
        bar_pref =1
    elif nochart_pref ==0:
        nochart_pref = 1 
    display_score =[]
    #max_pref =[]
    my_dict["line_pref"].append(line_pref)
    my_dict["bar_pref"].append(bar_pref)
    my_dict["nochart_pref"].append(nochart_pref)
    max_val = max(my_dict.items(), key=operator.itemgetter(1))[0]
    #max_val=max(max_pref)
    #print(max_val)
    
    #line_pref = int(line_pref)
    #bar_pref = int(bar_pref)
    #no_chart_pref = int(no_chart_pref)
    #print(type(line_pref))
    for index, row in meaningful_messages_final.iterrows():
        display_pref = row['psdo:PerformanceSummaryDisplay{Literal}']
        display_pref = display_pref.replace("'", "")
        x = display_pref.split(",")
        bar='bar'
        line='line'
        text='none'
        if bar in x:
            row['score'] = row['score']*bar_pref
        if line in x:
            row['score'] = row['score']*line_pref
        if text in x :
            row['score'] = row['score']*nochart_pref
        display_score.append(row['score'])

    meaningful_messages_final['display_score'] = display_score
    
    return meaningful_messages_final,max_val

def messagepreferences(display_preferences,message_preferences_df):
    #message_preferences_df.to_csv('before_select.csv')
    top_performer_pref=float(message_preferences_df.at[0,'Utilities.Message_Format.1'])
    nontop_performer_pref=float(message_preferences_df.at[0,'Utilities.Message_Format.2'])
    performance_dropped_below_peer_pref=float(message_preferences_df.at[0,'Utilities.Message_Format.16'])
    no_message_pref=float(message_preferences_df.at[0,'Utilities.Message_Format.24'])
    may_improve_pref=float(message_preferences_df.at[0,'Utilities.Message_Format.18'])
    approaching_goal_pref=float(message_preferences_df.at[0,'Utilities.Message_Format.11'])
    performance_improving_pref = float(message_preferences_df.at[0,'Utilities.Message_Format.22'])
    getting_worse_pref = float(message_preferences_df.at[0,'Utilities.Message_Format.14'])
    adverse_event_pref = float(message_preferences_df.at[0,'Utilities.Message_Format.21'])
    message_score = []
    if top_performer_pref == 0:
        top_performer_pref= 1
    elif nontop_performer_pref== 0:
        nontop_performer_pref =1
    elif performance_dropped_below_peer_pref ==0:
        performance_dropped_below_peer_pref = 1 
    elif approaching_goal_pref ==0:
        approaching_goal_pref = 1
    elif getting_worse_pref ==0:
        getting_worse_pref = 1
    #print(top_performer_pref,nontop_performer_pref,performance_dropped_below_peer_pref ,approaching_goal_pref,getting_worse_pref )
    for index, row in display_preferences.iterrows():
        #message_pref = row['display_score']
        text=row['psdo:PerformanceSummaryTextualEntity{Literal}']
        #x = text.split(" ")
        #print(x)
        if text == "1" :
            row['display_score'] = row['display_score']*top_performer_pref
        if text == "2":
            row['display_score'] = row['display_score']*nontop_performer_pref
        #if (top and not not1 in x) or (reached and goal in x) or (reached and benchmark in x) or(above and goal in x):
            
        if text == "16":
            row['display_score'] = row['display_score']*performance_dropped_below_peer_pref
        if text == "24":
            row['display_score'] = row['display_score']*no_message_pref
        if text == "18":
            row['display_score'] = row['display_score']*may_improve_pref
        if text == "11":
            row['display_score'] = row['display_score']*approaching_goal_pref
        if text == "22":
            row['display_score'] = row['display_score']*performance_improving_pref
        if text == "14":
            row['display_score'] = row['display_score']*getting_worse_pref
        if text == "21":
            row['display_score'] = row['display_score']*adverse_event_pref
        message_score.append(row['display_score'])
    display_preferences['message_score'] = message_score
    return display_preferences


def apply_history_message(applied_individual_messages,history,max_val,message_code):
    message_code_df = pd.json_normalize(message_code)
    history_df =pd.json_normalize(history)
    #history_df.to_csv("history_df.csv")
    month1 = history_df[['History.Month1.psdo:PerformanceSummaryDisplay{Literal}','History.Month1.Measure Name','History.Month1.Message Code']].copy()
    month2 = history_df[['History.Month2.psdo:PerformanceSummaryDisplay{Literal}','History.Month2.Measure Name','History.Month2.Message Code']].copy()
    month3 = history_df[['History.Month3.psdo:PerformanceSummaryDisplay{Literal}','History.Month3.Measure Name','History.Month3.Message Code']].copy()
    month4 = history_df[['History.Month4.psdo:PerformanceSummaryDisplay{Literal}','History.Month4.Measure Name','History.Month4.Message Code']].copy()
    month5 = history_df[['History.Month5.psdo:PerformanceSummaryDisplay{Literal}','History.Month5.Measure Name','History.Month5.Message Code']].copy()
    month6 = history_df[['History.Month6.psdo:PerformanceSummaryDisplay{Literal}','History.Month6.Measure Name','History.Month6.Message Code']].copy()
    applied_individual_messages.reset_index()
    for index, row in applied_individual_messages.iterrows():
        disp=row['psdo:PerformanceSummaryDisplay{Literal}'].split(",")
        if (month1['History.Month1.psdo:PerformanceSummaryDisplay{Literal}'][0] in disp and month1['History.Month1.Measure Name'][0]== row['Measure Name'] and month1['History.Month1.Message Code'][0]== row['psdo:PerformanceSummaryTextualEntity{Literal}'] ):
            applied_individual_messages = applied_individual_messages.drop(index)
        if (month2['History.Month2.psdo:PerformanceSummaryDisplay{Literal}'][0] in disp and month2['History.Month2.Measure Name'][0]== row['Measure Name'] and month2['History.Month2.Message Code'][0]== row['psdo:PerformanceSummaryTextualEntity{Literal}'] ):
            applied_individual_messages = applied_individual_messages.drop(index)
        if (month3['History.Month3.psdo:PerformanceSummaryDisplay{Literal}'][0] in disp and month3['History.Month3.Measure Name'][0]== row['Measure Name'] and month3['History.Month3.Message Code'][0]== row['psdo:PerformanceSummaryTextualEntity{Literal}'] ):
            applied_individual_messages = applied_individual_messages.drop(index)
        if (month4['History.Month4.psdo:PerformanceSummaryDisplay{Literal}'][0] in disp and month4['History.Month4.Measure Name'][0]== row['Measure Name'] and month4['History.Month4.Message Code'][0]== row['psdo:PerformanceSummaryTextualEntity{Literal}'] ):
            applied_individual_messages = applied_individual_messages.drop(index)
        if (month5['History.Month5.psdo:PerformanceSummaryDisplay{Literal}'][0] in disp and month5['History.Month5.Measure Name'][0]== row['Measure Name'] and month5['History.Month5.Message Code'][0]== row['psdo:PerformanceSummaryTextualEntity{Literal}'] ):
            applied_individual_messages = applied_individual_messages.drop(index)
        if (month6['History.Month6.psdo:PerformanceSummaryDisplay{Literal}'][0] in disp and month6['History.Month6.Measure Name'][0]== row['Measure Name'] and month6['History.Month6.Message Code'][0]== row['psdo:PerformanceSummaryTextualEntity{Literal}'] ):
            applied_individual_messages = applied_individual_messages.drop(index)
    return applied_individual_messages










def select(applied_individual_messages,max_val,message_code):
    # max value of score
    column = applied_individual_messages["message_score"]
    message_code_df = pd.json_normalize(message_code)
    #message_code_df.to_csv("message_code.csv")
    # max_value = column.max()
    h = applied_individual_messages["message_score"].idxmax()
    message_selected_df = applied_individual_messages.iloc[h, :]
    message_selected_df.at['psdo:PerformanceSummaryDisplay{Literal}']=max_val
    #message_selected_df.to_csv('message_selected.csv')
    mes_id=message_selected_df.at['psdo:PerformanceSummaryTextualEntity{Literal}'].split(".")
    #print(mes_id[0])
    message = "Message_ids."+mes_id[0]
    message_selected_df = message_selected_df.append(pd.Series(message_selected_df.at['psdo:PerformanceSummaryTextualEntity{Literal}'], index=['Message Code']))
    message_selected_df.at['psdo:PerformanceSummaryTextualEntity{Literal}']=message_code_df.at[0,message]
    message_selected_df   = message_selected_df.drop(['score','display_score','message_score']);
    message_selected_df = message_selected_df.T
    data = message_selected_df.to_json(orient="index", indent=2 )
    
    return data.replace("\\", "")
    #return column