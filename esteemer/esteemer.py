import warnings
import time
import logging
import random
import io
#from asyncore import read
from io import StringIO
from rdflib import Literal, URIRef, BNode
from rdflib.namespace import RDF



# from .load_for_real import load
# from load import read, transform,read_contenders,read_measures,read_comparators
# from score import score, select,apply_indv_preferences,apply_history_message

# load()

warnings.filterwarnings("ignore")
# TODO: process command line args if using graph_from_file()
# Read graph and convert to dataframe
start_time = time.time()
class Esteemer():
    def __init__(self, spek_tp,measure_list, preferences , history,mpm_df):
        self.y=[]
        self.spek_tp=spek_tp
        self.preferences=preferences
        self.history=history
        self.mpm_df=mpm_df
        self.s=URIRef("http://example.com/app#display-lab")
        self.p=URIRef("http://example.com/slowmo#HasCandidate")
        self.p1=URIRef("slowmo:acceptable_by")
        self.p2=URIRef('http://example.com/slowmo#Score')
        self.o2=Literal(1)
        self.gap_dicts={}
        self.trend_slopes={}
        self.losses={}
        self.acheivements={}
        self.measure_list=measure_list
        for s,p,o in self.spek_tp.triples( (self.s, self.p, None) ):
            s1= o
            for s,p,o in self.spek_tp.triples((s1,self.p1,None)):
                self.spek_tp.add((s,self.p2,self.o2))
                self.y.append(s)
                # print(s)
    def process_spek(self):
        # print(*self.y)
        sh=BNode("p1")
        ph=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
        p4=URIRef("http://example.com/slowmo#RegardingMeasure")
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
        loss.append("loss")
        acheivement=[]
        acheivement.append("acheivement")
        gaps=[]
        gaps.append("gaps")
        trend_slope=[]
        trend_slope.append("slopes")
        Measure4=None
        Measure =None
        Measure1=None
        Measure2=None
        Measure3=None
        # measure_list=self.performance_data_df["measure"].drop_duplicates()
        # print
        for x in self.measure_list:
            Measure=x
            for ss,ps,os in self.spek_tp.triples((sh,ph,None)):
                s6=os
                # print(s6)
                # for s122,p122,o122 in self.spek_tp.triples((s6,p4,None)):
                #     print(o122)
                #     print("\n")
                for s123,p123,o123 in self.spek_tp.triples((s6,ph33,None)):
                    #print(o123)
                    # print("\n")
                    if o123 == ph5 or o123 == ph6 :
                        for s124,p124,o124 in self.spek_tp.triples((s6,p4,None)):
                            
                            # Measure=o124
                            # print(o124)
                            if o124 == Measure:
                                for s125,p125,o125 in self.spek_tp.triples((s6,ph9,None)):
                                    gaps.append(o125)
                            # self.gap_dicts[o124]=o125
                            # print(o125)
            


                for s1234,p1234,o1234 in self.spek_tp.triples((s6,ph33,None)):
                    # print(o1234)
                    # print("\n")
                    if o1234 == ph3 or o1234 == ph4 :
                        for s127,p127,o127 in self.spek_tp.triples((s6,p4,None)):
                            
                            # print(o1234)
                            # print(o127)
                            
                            if o127 == Measure:
                                for s1254,p1254,o1254 in self.spek_tp.triples((s6,ph10,None)):
                                    # print(o1254)
                                    trend_slope.append(o1254)
                #                 # self.gap_dicts[o124]=o125
                #                 print(o1254)
                for s12345,p12345,o12345 in self.spek_tp.triples((s6,ph33,None)):
                    #print(o12345)
                    # print("\n")
                    if o12345 == ph8 :
                        for s129,p129,o129 in self.spek_tp.triples((s6,p4,None)):
                            
            #                 # print(o1234)
                            # print(o129)
                            # Measure=o129
                            if o129 ==Measure:
                                for s12546,p12546,o12546 in self.spek_tp.triples((s6,ph11,None)):
                                    # print(o12546)
                                    loss.append(o12546)
                # #                 # self.gap_dicts[o124]=o125
            # # 
                            # print(o1254)
                for s123456,p123456,o123456 in self.spek_tp.triples((s6,ph33,None)):
                    # print(o123456)
                    # print("\n")
                    if o123456 == ph7 :
                        for s130,p130,o130 in self.spek_tp.triples((s6,p4,None)):
                            
            # #                 # print(o1234)
                            #print(o130)
                            # Measure4=o130
                            if o130==Measure:
                                for s125467,p125467,o125467 in self.spek_tp.triples((s6,ph12,None)):
                                    # print(o12546)
                                    acheivement.append(o125467)
            
            if Measure is not None :
                # acheivement.append("acheivement")
                acheivement = list(set(acheivement))
                # acheivement.append("acheivement")
                self.acheivements[Measure]=acheivement
                for k,v in self.acheivements.items():print(k, v)
            if Measure is not None :
                # loss.append("loss")
                loss = list(set(loss))
                self.losses[Measure]=loss
                for k,v in self.losses.items():print(k, v)
            if Measure is not None :
                # trend_slope.append("slope")
                trend_slope = list(set(trend_slope))
                self.trend_slopes[Measure]=trend_slope   
                for k,v in self.trend_slopes.items():print(k, v)
            
            if Measure is not None :
                # gaps.append("gaps")
                gaps = list(set(gaps))
                self.gap_dicts[Measure]=gaps   
                for k,v in self.gap_dicts.items():print(k, v)             
                    
            
                
                
            # f = open("outputs/triple.txt", "a")
            # f.write(ss + "," + ps + "," + os)
            # f.write("\n") 
            
    def process_history(self):
        def extract(a):
    #recursive algorithm for extracting items from a list of lists and items
            if type(a) is list:
                l = []
                for item in a:
                    l+=extract(item)
                return l
            else:
                return [a]
        
        Message_received_count=[]
        causal_pathways=[]
        causal_pathways1=[]
        message_recency={}
        a=[]
        i=0
        for k,v in self.history.items():
            
            i=i+1
            for k1,v1 in v.items():
                # print(k)
                # print(k1)
                if k1 == "Text":
                    Message_received_count.append(v1)
                if k1=="Causal_pathways":
                    causal_pathways.append(v1)
                    # i=i+1
                    message_recency[i]=v1
                 
        causal_pathways=extract(causal_pathways)
        # print(*causal_pathways)
        for x in causal_pathways:
            x=x.replace("social ","")
            x=x.replace("goal ","")
            causal_pathways1.append(x)

            # print(x)
            # print("\n")
        # print(*causal_pathways1)
        my_dict = {i:causal_pathways1.count(i) for i in causal_pathways1}
        
        
        for k2,v2 in message_recency.items():
            print(k2,v2)


        
        # f.close()
    def select(self):
        self.scores=[]
        nodes=[]
        # print(*self.y)
        if len(self.y)!=0:
            self.node=random.choice(self.y)
        else:
            self.node="No message selected"

        if self.node== "No message selected":
            return self.node,self.spek_tp
        else:
            o2=URIRef("http://example.com/slowmo#selected")
            self.spek_tp.add((self.node,RDF.type,o2))
            return self.node,self.spek_tp

    def get_selected_message(self):
        s_m={}
        if self.node== "No message selected":
            s_m["text"]="No message selected"
            return s_m 
        else:
            s=self.node
            p1=URIRef("psdo:PerformanceSummaryTextualEntity")
            pwed=URIRef("slowmo:acceptable_by")
            p3=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
            p4=URIRef("http://example.com/slowmo#RegardingMeasure")
            p8=URIRef("http://example.com/slowmo#name")
            p10= URIRef("http://purl.org/dc/terms/title")
            p12=URIRef("http://purl.obolibrary.org/obo/IAO_0000573")
            p13=URIRef("http://purl.obolibrary.org/obo/STATO_0000166")
            p20=URIRef("http://example.com/slowmo#AncestorTemplate")
            pqd=URIRef("http://example.com/slowmo#PerformanceGapSize")
            pqw=URIRef("http://example.com/slowmo#PerformanceTrendSlope")
            p232= URIRef("psdo:PerformanceSummaryDisplay")
            Display=["Text-only", "bar chart", "line graph"]
            sw=0
            o2wea=[]
            
            
            for s21,p21,o21 in self.spek_tp.triples((s,p20,None)):
                s_m["Template ID"] = o21
            for s2,p2,o2 in self.spek_tp.triples((s,p1,None)):
                s_m["text"] = o2
            # for s212,p212,o212 in self.spek_tp.triples((s,p232,None)):
               
            s_m["Display"]=random.choice(Display)
            for s9,p9,o9 in self.spek_tp.triples((s,p8,None)):
                s_m["Comparator Type"] = o9
            for s2we,p2we,o2we in self.spek_tp.triples((s,pwed,None)):
                o2wea.append(o2we)
            # print(*o2wea)
            s_m["Acceptable By"] = o2wea

            
            
            

            
                
            

            for s5,p5,o5 in self.spek_tp.triples((s,p3,None)):
                s6=o5
                # print(o5)
                for s7,p7,o7 in self.spek_tp.triples((s6,p4,None)):
                    s_m["Measure Name"]=o7
                    s10= BNode(o7)
                    for s11,p11,o11 in self.spek_tp.triples((s10,p10,None)):
                        s_m["Title"]=o11
                for s14,p14,o14 in self.spek_tp.triples((s6,RDF.type,None)):
                    #print(o14)
                    if o14==p12:
                        s_m["Display"]="line graph"
                        sw=1
                    if o14==p13:
                        s_m["Display"]="bar chart"
                        if sw==1:
                            s_m["Display"]= "line graph,bar chart"
                

            
                  

            
            return s_m
    
# logging.critical("--score and select %s seconds ---" % (time.time() - start_time1))
# print(finalData)

# time_taken = time.time()-start_time
logging.critical("---total esteemer run time according python script %s seconds ---" % (time.time() - start_time))

"""with open('data.json', 'a') as f:
    f.write(finalData + '\n')"""
