import numpy as np 
import matplotlib.pyplot as plt 
import io
import base64
#from asyncore import read

import pandas as pd





class Pictoralist():

    def __init__(self, selected_message, performance_data: pd.DataFrame=()):
        self.selected_message_dict=selected_message
        self.performance_data = performance_data

        self.display_format = self.selected_message_dict["Display"]
        self.text= self.selected_message_dict["text"]
        self.measure_name= self.selected_message_dict["Measure Name"]
    
        self.title=self.selected_message_dict["Title"]
        self.comparator=self.selected_message_dict["Comparator Type"]
        self.comparison_value=0.9
        
    
    def create_graph(self):
        self.performance_data['Month']= pd.to_datetime(self.performance_data['Month'], errors='coerce')
        self.display_format=str(self.display_format)
        self.measure_name=str(self.measure_name)
        if self.display_format == "line graph,bar chart":
            self.display_format = "bar chart"
            # print(self.display_format)
        if self.display_format == "bar chart":
            # print(self.performance_data)
            self.graph_df = self.performance_data[self.performance_data['Measure_Name'] ==  self.measure_name]
            idx= self.graph_df.groupby(['Measure_Name'])['Month'].nlargest(4) .reset_index()
            l=idx['level_1'].tolist()
            self.last_4_measure =  self.performance_data[self.performance_data.index.isin(l)]
            # print(self.last_4_measure)
            
            # try:
            #     self.last_4_measure['performance_data'] =(self.last_4_measure['Passed_Count'] / self.last_4_measure['Denominator'])*100
            # except ZeroDivisionError:
            #     self.last_4_measure['performance_data'] =100
        #self.last_4_measure['performance_data'] =  self.last_4_measure['performance_data'].round(decimals = 1)
            self.comparison_value=self.comparison_value*100
            self.peer_average= self.last_4_measure["Peer_Average"]*100
            self.benchmark=[90,90,90,90]
            self.performance_data=self.last_4_measure['Performance_Rate']*100
        

            self.last_4_measure['Date'] = pd.to_datetime(self.last_4_measure['Month'])
            self.last_4_measure['year']= pd.DatetimeIndex(self.last_4_measure['Month']).year
            self.last_4_measure['month1'] = pd.DatetimeIndex(self.last_4_measure['Month']).month
            self.last_4_measure['year']=self.last_4_measure['year'].astype(str)
            self.last_4_measure['month1']=self.last_4_measure['month1'].astype(str)+"/"
            #X=self.last_4_measure['month1']+self.last_4_measure['year']
            self.last_4_measure['month2'] = self.last_4_measure['Month'].dt.strftime('%b')
            X=self.last_4_measure['month2']
            X_axis = np.arange(len(X))
        #plt.figure(figsize=(40,30))
            X_p=X_axis - 0.2
            X_b=X_axis + 0.2
            X_g = X_axis-0.4
            X_l = X_axis+0.9
            self.performance_data = self.performance_data.tolist()
            self.performance_data = [round(item, 2) for item in self.performance_data]
            # print(self.performance_data)
            self.peer_average = self.peer_average.tolist()
            plt.plot(X_g,self.benchmark, color="black",linestyle="--")
            plt.plot(X_l,self.benchmark, color="black",linestyle="--")
            line=plt.bar(X_p, self.performance_data, 0.4, label = 'Performance', color="#00274C")
            line1=plt.bar(X_b, self.peer_average, 0.4, label = 'Peer Average', color="#878A8F")
            for i in range(len(self.performance_data)):
                plt.annotate(str(self.performance_data[i]), xy=(X_p[i],self.performance_data[i]), ha='center', va='bottom',xytext=(X_p[i],self.performance_data[i]-10),color='white')
            for i in range(len(self.peer_average)):
                plt.annotate(str(self.peer_average[i]), xy=(X_b[i],self.peer_average[i]), ha='center', va='bottom',xytext=(X_b[i],self.peer_average[i]-10),color='white')
            plt.xticks(X_axis,X)
        
        #X=X.tolist()
            plt.xlim(left=-0.4)
        #plt.xlim(X[0],X[len(X)-1])
        #plt.xticks(rotation =45)
            plt.xlabel("Month")
            plt.ylabel("Performance")
            plt.title(self.text+"\n"+" for the measure "+self.measure_name+" ("+self.title+")")
            plt.legend(bbox_to_anchor=(1, 0), loc="lower right")
        #plt.legend(bbox_to_anchor=(-0.75, -0.15), loc="lower left")
        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox = True, shadow = True)
            #plt.show()
            plt.savefig("cache/cached1.png")
            # cached_img = open("cache/cached1.png")
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            return  s



        if self.display_format == 'line graph':
            self.graph_df = self.performance_data[self.performance_data['Measure_Name'] ==  self.measure_name]
            self.graph_df['Date'] = pd.to_datetime(self.graph_df['Month'])
            self.graph_df['year']= pd.DatetimeIndex(self.graph_df['Month']).year
            self.graph_df['month1'] = pd.DatetimeIndex(self.graph_df['Month']).month
            self.graph_df['year']=self.graph_df['year'].astype(str)
            self.graph_df['month1']=self.graph_df['month1'].astype(str)+"/"
            self.graph_df['month2'] = self.graph_df['Month'].dt.strftime('%b')
            #X=self.graph_df['month1']+self.graph_df['year']
            X = self.graph_df['month2']
            # try:
            #     self.graph_df['performance_data'] =(self.graph_df['Passed_Count'] / self.graph_df['Denominator'])*100
            # except ZeroDivisionError:
            #     self.graph_df['performance_data'] =100
            self.performance_data=self.graph_df['Performance_Rate']*100
            #print(self.performance_data)
            self.peer_average=self.graph_df['Peer_Average']*100
            self.performance_data = self.performance_data.tolist()
            self.benchmark=[90,90,90,90,90,90,90,90,90,90,90,90]
            self.performance_data = [round(item, 2) for item in self.performance_data]
            arr1=plt.plot(X,self.performance_data,color="#00274C")
            arr2=plt.plot(X,self.peer_average,color="#00B5AF")
            arr3=plt.plot(X,self.benchmark, linestyle="--", color="black")
            plt.xlim(left= -0.1)
            plt.ylim(0,120)
            plt.xlabel("Month")
            plt.ylabel("Performance")
            plt.title(self.text+"\n"+" for the measure "+self.measure_name +" ("+self.title+")")
            plt.legend(["Your Performance","Peers","Benchmark"])
            #plt.show()
            plt.savefig("cache/cached1.png")
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            return  s

        #self.last_4_measure.to_csv("last4measure.csv")
        

        
