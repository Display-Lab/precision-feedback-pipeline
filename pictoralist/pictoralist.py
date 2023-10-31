import numpy as np 
import matplotlib.pyplot as plt 
import io
import base64
import numpy
import pandas as pd
import json
import datetime



## Pictoralist Mk II
class Pictoralist():

    def __init__(self, selected_message, p_df, generate_image, performance_data_df: pd.DataFrame=()):
        ## Esteemer output, Selected Message
        self.selected_message_dict=selected_message # try to print this to better understand the architecture
        print(self.selected_message_dict)
        self.performance_data = performance_data_df
        self.Performance_Data = performance_data_df     # duplicate, in use still though lol
        self.performance_Data=p_df
        print(f"\n\n\n\np_df is\n\n{p_df}\n\n\nperf data df is:\n\n{performance_data_df}")
        
        self.template= self.selected_message_dict["Template ID"]
        self.display_format = self.selected_message_dict["Display"]
        self.text= self.selected_message_dict["text"]
        self.measure_name= self.selected_message_dict["Measure Name"]
        self.acceptable_by = self.selected_message_dict["Acceptable By"]
        self.title=self.selected_message_dict["Title"]
        self.comparator=self.selected_message_dict["Comparator Type"]
        self.comparison_value=0.9
        ## Init flag for image generation, defaults to true
        self.generate_image = generate_image
        
    
    def create_graph(self):
        self.performance_data['month']= pd.to_datetime(self.performance_data['month'], errors='coerce')
        self.display_format=str(self.display_format)
        self.measure_name=str(self.measure_name)
        # if self.display_format == "Text-only, bar chart, line chart":
        #     self.display_format = "bar chart"
        print(self.display_format)
        
        ## Control logic for image-less feedback generation:
        if self.generate_image:
            if self.display_format == "bar chart":
                # print(self.performance_data)
                self.graph_df = self.performance_data[self.performance_data['measure'] ==  self.measure_name]
                idx= self.graph_df.groupby(['measure'])['month'].nlargest(4) .reset_index()
                l=idx['level_1'].tolist()
                self.last_4_measure =  self.performance_data[self.performance_data.index.isin(l)]
                # print(self.last_4_measure)

                # try:
                #     self.last_4_measure['performance_data'] =(self.last_4_measure['Passed_Count'] / self.last_4_measure['Denominator'])*100
                # except ZeroDivisionError:
                #     self.last_4_measure['performance_data'] =100
            #self.last_4_measure['performance_data'] =  self.last_4_measure['performance_data'].round(decimals = 1)
                self.comparison_value=self.comparison_value*100
                self.peer_average= self.last_4_measure["peer_average_comparator"]*100
                self.benchmark=[90,90,90,90]
                self.performance_data=self.last_4_measure['Performance_Rate']*100


                self.last_4_measure['Date'] = pd.to_datetime(self.last_4_measure['month'])
                self.last_4_measure['year']= pd.DatetimeIndex(self.last_4_measure['month']).year
                self.last_4_measure['month1'] = pd.DatetimeIndex(self.last_4_measure['month']).month
                self.last_4_measure['year']=self.last_4_measure['year'].astype(str)
                self.last_4_measure['month1']=self.last_4_measure['month1'].astype(str)+"/"
                #X=self.last_4_measure['month1']+self.last_4_measure['year']
                self.last_4_measure['month2'] = self.last_4_measure['month'].dt.strftime('%b')
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
                self.selected_message_dict["image"]=s
                return  s



            if self.display_format == 'line graph':
                self.graph_df = self.performance_data[self.performance_data['measure'] ==  self.measure_name]
                self.graph_df['Date'] = pd.to_datetime(self.graph_df['month'])
                self.graph_df['year']= pd.DatetimeIndex(self.graph_df['month']).year
                self.graph_df['month1'] = pd.DatetimeIndex(self.graph_df['month']).month
                self.graph_df['year']=self.graph_df['year'].astype(str)
                self.graph_df['month1']=self.graph_df['month1'].astype(str)+"/"
                self.graph_df['month2'] = self.graph_df['month'].dt.strftime('%b')
                #X=self.graph_df['month1']+self.graph_df['year']
                X = self.graph_df['month2']
                # try:
                #     self.graph_df['performance_data'] =(self.graph_df['Passed_Count'] / self.graph_df['Denominator'])*100
                # except ZeroDivisionError:
                #     self.graph_df['performance_data'] =100
                self.performance_data=self.graph_df['Performance_Rate']*100
                #print(self.performance_data)
                self.peer_average=self.graph_df['peer_average_comparator']*100
                self.performance_data = self.performance_data.tolist()
                self.benchmark=[90,90,90,90,90,90,90,90,90,90,90,90]
                self.performance_data = [round(item, 2) for item in self.performance_data]
                arr1=plt.plot(X,self.performance_data,color="#00274C")
                arr2=plt.plot(X,self.peer_average,color="#00B5AF")
                arr3=plt.plot(X,self.benchmark, linestyle="--", color="black")
                plt.xlim(left= -0.1)
                plt.ylim(0,120)
                plt.xlabel("month")
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
        else:
            ## When no image is generated, make sure the field is empty:
            self.selected_message_dict["image"] = ""
        

        #self.last_4_measure.to_csv("last4measure.csv")

    def prepare_selected_message(self):
        candidate={}
        message={}
        candidate["message_template"]=self.template
        candidate["display"]=self.display_format
        candidate["measure"]=self.measure_name
        candidate["acceptable_by"]=self.acceptable_by
        message["text_message"]=self.text
        message["measure"]=self.measure_name
        message["title"]=self.title
        message["comparison_value"]=0.9
        # message["recipient_performance_level"]
        #print(type(self.performance_Data))
        self.Performance_Data=self.Performance_Data[self.Performance_Data['measure'] ==  self.measure_name]
        #print(self.Performance_Data)
        staff_number= self.Performance_Data['staff_number'].iloc[0]
        array = self.performance_Data
        ds=pd.DataFrame(self.performance_Data)
        # print(ds)
        ds.columns=ds. iloc[0]
        
        self.performance_Data=ds[ds['measure'] ==  self.measure_name]
        self.performance_Data=self.performance_Data.values.tolist()
        ar = numpy.array(self.performance_Data)
        df2 = json.dumps(self.performance_Data)
        df3= ','.join(str(x) for x in ar)
        df4=df3.replace('\n', '')
        performance_month = self.Performance_Data.iloc[-1]
        #print(type(performance_month))
        performance_month_1 = performance_month['month']
        recipient_performance_level=performance_month['Performance_Rate']
        
        message_generated_datetime= datetime.datetime.now()
        pfkb_version="1.0.1"
        pfp_version="1.2.2"
        self.comparator=str(self.comparator)

        # print(performance_month)
        # print(self.comparator)
        if self.comparator == "lost top 10 benchmark":
            message["comparison_value"]=performance_month['peer_90th_percentile_benchmark']
            # message["comparison_value"]=performance_month['peer_90th_percentile_benchmark']
        if self.comparator == "Top 25 Performer":
            message["comparison_value"]=performance_month['peer_75th_percentile_benchmark']
        if self.comparator == "Top 10 Performer":
            message["comparison_value"]=performance_month['peer_90th_percentile_benchmark']
        if self.comparator == "Lost Peer Average":
            message["comparison_value"]=performance_month['peer_average_comparator']
        message["recipient_performance_level"]=recipient_performance_level*100
        # if self.display_format == "bar chart" and self.display_format == "line graph":
        message["image"]=self.selected_message_dict["image"]
        # message["image"]=self.selected_message_dict["image"]

        selected_message1={"staff_number":staff_number,
                           "selected_candidate":candidate,
                           "performance_data":df4,
                           "performance_month":performance_month_1,
                           "message_generated_datetime":message_generated_datetime,
                           "pfkb_version":pfkb_version,
                           "pfp_version":pfp_version,
                           "Message":message
                           }
        
        return selected_message1


        