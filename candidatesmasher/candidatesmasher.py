import warnings


import warnings


import pandas as pd
from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF



warnings.filterwarnings("ignore", category=FutureWarning)
class CandidateSmasher:
    def __init__(self,spek_bs:Graph,templates:Graph):
        self.a=spek_bs
        self.b=templates
        self.measure_dicts={}
        self.social_dicts={}
        self.goal_dicts={}
        self.social_comparison_dicts={}
        self.goal_comparison_dicts={}
        self.annotate_dicts={}
        self.graph_type_list=[]
        self.asd=[]



        self.so=URIRef("http://example.com/app#display-lab")
        self.sq12=URIRef("http://example.com/app#display-lab")
        self.pq12=URIRef("http://example.com/slowmo#HasCandidate")
        self.po=URIRef('http://example.com/slowmo#IsAboutMeasure')
        self.p1=URIRef("http://example.com/slowmo#WithComparator")
        self.p3=URIRef('http://schema.org/name')
        self.o5=URIRef("http://purl.obolibrary.org/obo/psdo_0000095")
        self.p5=RDF.type
        self.p6=URIRef("http://example.com/slowmo#ComparisonValue")
        self.p21=URIRef("http://purl.org/dc/terms/title")
        self.p22=URIRef("http://schema.org/name")
        self.o21=Literal("PEERS")
        self.o22=Literal("peers") 
        self.p23=URIRef("http://schema.org/name")
        self.p24=URIRef("http://purl.obolibrary.org/obo/IAO_0000136")
        self.p25=RDF.type
        self.pq13=URIRef("psdo:PerformanceSummaryDisplay")
        self.pq14=URIRef("psdo:PerformanceSummaryTextualEntity")
        self.pq15=URIRef("http://schema.org/name")
        self.pf234=URIRef("Display compatibility")

        self.cp=RDF.type
        self.co=URIRef("http://purl.obolibrary.org/obo/cpo_0000053")
        self.cp1=URIRef("http://example.com/slowmo#name")
        self.cp2=URIRef("psdo:PerformanceSummaryTextualEntity")
        self.cp3=URIRef("psdo:PerformanceSummaryDisplay")
        self.cp4=RDF.type
        self.cop4=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
        self.cp23=URIRef("http://example.com/slowmo#RegardingComparator")
        self.cp24=URIRef("http://example.com/slowmo#RegardingMeasure")
        self.cp25="http://purl.obolibrary.org/obo/PSDO_0000102"
        self.cp26=URIRef("http://example.com/slowmo#AncestorPerformer")
        self.cp27=URIRef("http://example.com/slowmo#AncestorTemplate")
        self.cp28=URIRef("http://example.com/slowmo#Candidate")
        self.message_text=URIRef("https://schema.metadatacenter.org/properties/6b9dfdf9-9c8a-4d85-8684-a24bee4b85a8")
        self.display=URIRef("https://schema.metadatacenter.org/properties/6b9dfdf9-9c8a-4d85-8684-a24bee4b85a8123")
        self.bar_chart=URIRef("http://purl.obolibrary.org/obo/STATO_0000166")
        self.line_graph=URIRef("http://purl.obolibrary.org/obo/IAO_0000573")
        self.display_format=URIRef("https://schema.metadatacenter.org/properties/08244d65-5f32-4ef5-829f-5075a936234f")

        self.cp21=URIRef("http://example.com/slowmo#AncestorTemplate")
# f1 = open("test23.txt", "w")
# f2 = open("test24.txt", "w")
        self.ac=[]
        self.ab=[]
        self.text_dicts={}
        self.name_dicts={}
        # self.display_dicts={}
        self.template_type_dicts={}
        self.candidate_id_dicts={}
        self.goal_dicts={}
        self.peer_dicts={}
        self.top_10_dicts={}
        self.top_25_dicts={}
        self.graph_type_list=[]
        self.graph_type_list1=[]

    def get_graph_type(self):
        for s,p,o in self.a.triples((self.so, self.po, None)):
            s1=o
            goal_nodes=[]
            for s2,p2,o2 in self.a.triples((s1,self.p1,None)):
                
                self.measure_dicts[s1]=o2
                s3=o2
                final_node_type=[]
                node_type=[]
                node_type1=[]
                node_type2=[]
                node_type.append(s1)
                node_type.append(o2)
                for s4,p4,o4 in self.a.triples((s3,self.p3,None)):
                        #print(o4)
                        if str(o4)=="peers":
                            self.peer_dicts[s1]=o2
                        if str(o4)=="goal":
                            self.goal_dicts[s1]=o2
                        if str(o4)=="top_10":
                            self.top_10_dicts[s1]=o2
                        if str(o4)=="top_25":
                            self.top_25_dicts[s1]=o2
                        
                
                # self.a.remove((s1,self.p1,o2))
                # for s2,p2,o21 in self.a.triples((s1,self.p1,None)):
                #     #self.goal_dicts[s1]=o2
                #     self.a.remove((s1,self.p1,o21))
                #     for s2,p2,o212 in self.a.triples((s1,self.p1,None)):
                #         print(o212)
                # self.a.add((s1,self.p1,o2))
            # 
            
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if str(o82) != self.cp25:
                        # print(o82)
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        node_type.append(node_tuple)
        
                    
            node_type_tuple=tuple(node_type)
        
            self.graph_type_list.append(node_type_tuple)
        # print(*self.graph_type_list)
        anew = pd.DataFrame.from_dict(self.peer_dicts, orient ='index')
        anew= anew.reset_index()
        anew = anew.rename({"index":"measure"}, axis=1)
        anew = anew.rename({0:"Comparator_Node"}, axis=1)
        self.peer_types=[]
        for rowIndex, row in anew.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            node_type122=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type122:
                        node_type122.append(s1)
                    if o2 not in node_type122:
                        node_type122.append(o2)
                    if str(o82) != self.cp25:
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        node_type122.append(node_tuple)
            node_type_tuple122=tuple(node_type122)
            node_type_tuple122=node_type_tuple122
            self.peer_types.append(node_type_tuple122)
        # print(*self.peer_types)
        new = pd.DataFrame.from_dict(self.goal_dicts, orient ='index')
        new= new.reset_index()
        new = new.rename({"index":"measure"}, axis=1)
        new = new.rename({0:"Comparator_Node"}, axis=1)
        self.goal_types=[]
        for rowIndex, row in new.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            node_type1=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type1:
                        node_type1.append(s1)
                    if o2 not in node_type1:
                        node_type1.append(o2)
                    if str(o82) != self.cp25:
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        node_type1.append(node_tuple)
            node_type_tuple1=tuple(node_type1)
            node_type_tuple1=node_type_tuple1
            self.goal_types.append(node_type_tuple1)
        # print(*self.goal_types)
        new1 = pd.DataFrame.from_dict(self.top_10_dicts, orient ='index')
        new1= new1.reset_index()
        new1 = new1.rename({"index":"measure"}, axis=1)
        new1 = new1.rename({0:"Comparator_Node"}, axis=1)
        self.top_10_types=[]
        for rowIndex, row in new1.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            node_type2=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type2:
                        node_type2.append(s1)
                    if o2 not in node_type2:
                        node_type2.append(o2)
                    if str(o82) != self.cp25:
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        node_type2.append(node_tuple)
                        # node_type2.append(str(o82))
            node_type_tuple2=tuple(node_type2)
            node_type_tuple2=node_type_tuple2
            self.top_10_types.append(node_type_tuple2)
        # print(*self.top_10_types)
        new2 = pd.DataFrame.from_dict(self.top_25_dicts, orient ='index')
        new2= new2.reset_index()
        new2 = new2.rename({"index":"measure"}, axis=1)
        new2 = new2.rename({0:"Comparator_Node"}, axis=1)
        # new2.to_csv("top_25.csv")
        self.top_25_types=[]
        for rowIndex, row in new2.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            node_type3=[]
            for  s81,p81,o81 in self.a.triples((None, None,o2)):
                for s82,p82,o82 in self.a.triples((s81,RDF.type,None)):
                    if s1 not in node_type3:
                        node_type3.append(s1)
                    if o2 not in node_type3:
                        node_type3.append(o2)
                    if str(o82) != self.cp25:
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        node_type3.append(node_tuple)
                        # node_type3.append(str(o82))
            node_type_tuple3=tuple(node_type3)
            node_type_tuple3=node_type_tuple3
            self.top_25_types.append(node_type_tuple3)
        
        self.df_graph = pd.DataFrame(self.peer_types)
        # self.peer_graph = pd.DataFrame(self.peer_types)
        # self.df_graph.to_csv("peer_types.csv")
        self.goal_types=pd.DataFrame(self.goal_types)
        self.top_10_types=pd.DataFrame(self.top_10_types)
        self.top_25_types=pd.DataFrame(self.top_25_types)
        self.df_graph = self.df_graph.rename({0:"measure"}, axis=1)
        self.df_graph = self.df_graph.rename({1:"Comparator_Node1"}, axis=1)
        if 2 in self.df_graph:
            self.df_graph = self.df_graph.rename({2:"graph_type1"}, axis=1)
        if 3 in self.df_graph:
            self.df_graph = self.df_graph.rename({3:"graph_type2"}, axis=1)
        if 4 in self.df_graph:
            self.df_graph = self.df_graph.rename({4:"graph_type3"}, axis=1)
        if 5 in self.df_graph:
            self.df_graph = self.df_graph.rename({5:"graph_type4"}, axis=1)
        if 6 in self.df_graph:    
            self.df_graph = self.df_graph.rename({6:"graph_type5"}, axis=1)
        if 7 in self.df_graph:
            self.df_graph = self.df_graph.rename({7:"graph_type6"}, axis=1)
        self.df_graph = self.df_graph.fillna(0)
        self.df_graph["comparator_type"]="peers"
        self.df_graph=self.df_graph.reset_index(drop=True)
        self.df_graph = self.df_graph.drop('Comparator_Node1', axis=1)
        # self.df_graph = self.df_graph.drop('comparator_type', axis=1)
        # self.df_graph.to_csv("graph_df.csv")
        # self.df_graph1=pd.DataFrame(self.graph_type_list1)
        self.goal_types = self.goal_types.rename({0:"measure"}, axis=1)
        self.goal_types = self.goal_types.rename({1:"Comparator_Node"}, axis=1)
        self.goal_types = self.goal_types.rename({2:"graph_type1"}, axis=1)
        self.goal_types = self.goal_types.rename({3:"graph_type2"}, axis=1)
        self.goal_types = self.goal_types.rename({4:"graph_type3"}, axis=1)
        self.goal_types = self.goal_types.rename({5:"graph_type4"}, axis=1)
        self.goal_types = self.goal_types.rename({6:"graph_type5"}, axis=1)
        self.goal_types = self.goal_types.rename({7:"graph_type6"}, axis=1)
        self.goal_types = self.goal_types.fillna(0)
        self.goal_types["comparator_type"]="goal"
        self.goal_types = self.goal_types.drop('Comparator_Node', axis=1)
        self.goal_types=self.goal_types.reset_index(drop=True)
        # self.goal_types.to_csv("goal_types.csv")


        self.top_10_types = self.top_10_types.rename({0:"measure"}, axis=1)
        self.top_10_types = self.top_10_types.rename({1:"Comparator_Node"}, axis=1)
        self.top_10_types = self.top_10_types.rename({2:"graph_type1"}, axis=1)
        self.top_10_types = self.top_10_types.rename({3:"graph_type2"}, axis=1)
        self.top_10_types = self.top_10_types.rename({4:"graph_type3"}, axis=1)
        self.top_10_types = self.top_10_types.rename({5:"graph_type4"}, axis=1)
        self.top_10_types = self.top_10_types.rename({6:"graph_type5"}, axis=1)
        self.top_10_types = self.top_10_types.rename({7:"graph_type6"}, axis=1)
        self.top_10_types = self.top_10_types.fillna(0)
        self.top_10_types["comparator_type"]="top10_types"
        self.top_10_types=self.top_10_types.reset_index(drop=True)
        self.top_10_types= self.top_10_types.drop('Comparator_Node', axis=1)
        # self.top_10_types = self.top_10_types.drop('comparator_type', axis=1)
        # self.top_10_types.to_csv("top_10_types.csv")

        self.top_25_types = self.top_25_types.rename({0:"measure"}, axis=1)
        self.top_25_types = self.top_25_types.rename({1:"Comparator_Node"}, axis=1)
        self.top_25_types = self.top_25_types.rename({2:"graph_type1"}, axis=1)
        self.top_25_types = self.top_25_types.rename({3:"graph_type2"}, axis=1)
        self.top_25_types = self.top_25_types.rename({4:"graph_type3"}, axis=1)
        self.top_25_types = self.top_25_types.rename({5:"graph_type4"}, axis=1)
        self.top_25_types = self.top_25_types.rename({6:"graph_type5"}, axis=1)
        self.top_25_types = self.top_25_types.rename({7:"graph_type6"}, axis=1)
        self.top_25_types = self.top_25_types.fillna(0)
        self.top_25_types["comparator_type"]="top25_types"
        self.top_25_types=self.top_25_types.reset_index(drop=True)
        self.top_25_types= self.top_25_types.drop('Comparator_Node', axis=1)
        # self.top_25_types = self.top_25_types.drop('comparator_type', axis=1)
        # self.top_25_types.to_csv("top_25_types.csv")

        # dfs1 = [self.df_graph, self.top_10_types, self.top_25_types]
        self.df_merged = pd.concat([self.goal_types,self.df_graph,self.top_10_types,self.top_25_types], ignore_index=True, sort=False)
        dfs=self.df_graph.merge(self.top_10_types,on='measure').merge(self.top_25_types,on='measure')
        # dfs["comparator_type"]="peers"
        # self.df_merged.to_csv("dfs1.csv")
        # self.df_merged = pd.concat([dfs, self.goal_types], ignore_index=True, sort=False)
        # self.df_merged =self.df_merged.fillna(0)
        
        self.df_merged.to_csv("df_merged.csv")
        return self.df_merged,self.goal_types,self.df_graph,self.top_10_types,self.top_25_types

       

    def get_template_data(self):
        # for triple in self.b.triples((None,None,None)):
        #     print(triple)
    
        for s,p,o in self.b.triples((None,self.p23,None)):
            self.ac.append(str(o))
        # print(*self.ac)
        
        for sq,pq,oq in self.b.triples((None,self.p3,None)):
            self.asd.append(str(sq))

        # a25_dicts={}
        a26_dicts={}
        a27_dicts={}
        a278_dicts={}
        templatetype_dicts={}
        for x in range(len(self.asd)):
            s24=URIRef(self.asd[x])
            
            af=[]
            ab=[]
            # for s29,p29,o29 in self.b.triples((s24,self.display_format,None)):
            #     a253=str(o29)
            #     af.append(a253)
            # afd=tuple(af)
            # a25_dicts[s24]=afd
        #     for s30,p30,o30 in self.b.triples((s24,self.pq14,None)):
        #         a26_dicts[self.ac[x]]=str(o30)
            for s30,p30,o30 in self.b.triples((s24,self.message_text,None)):
                # print(str(o30))
                a26_dicts[s24]=str(o30)
            for s31,p31,o31 in self.b.triples((s24,self.pq15,None)):
                a27_dicts[s24]=str(o31)
            for s322,p322,o322 in self.b.triples((s24,self.display,None)):
                a278_dicts[s24]=str(o322)

            for s,p,o in self.b.triples((s24,self.p24,None)):
                templatetype=str(o)
                ab.append(templatetype)
            #     s25=o
            #     for s,p,o in self.b.triples((s25,self.p25,None)):
            #         templatetype=str(o)
            #         ab.append(templatetype)
            ad=tuple(ab)
            # print(s24)
            # print(ad)
            templatetype_dicts[s24]=ad
           
        
          
        # display_dicts=a25_dicts
        text_dicts=a26_dicts
        name_dicts=a27_dicts
        # display_dicts=a278_dicts
        template_type_dicts=templatetype_dicts
        # for k,v in text_dicts.items():
        #     print(k,v)
        self.df_text = pd.DataFrame.from_dict(text_dicts,orient='index')
        self.df_text = self.df_text.rename({0:"text"}, axis=1)
        # self.df_display_dicts=pd.DataFrame.from_dict(display_dicts,orient='index')
        # self.df_display_dicts = self.df_display_dicts.rename({0:"display"}, axis=1)
        # self.df_display_dicts = self.df_display_dicts.rename({1:"display2"}, axis=1)
        self.df_name_dicts=pd.DataFrame.from_dict(name_dicts,orient='index')
        self.df_name_dicts = self.df_name_dicts.rename({0:"name"}, axis=1)
        self.df_template_type_dicts=pd.DataFrame.from_dict(template_type_dicts,orient='index')
        self.df_template_type_dicts = self.df_template_type_dicts.rename({0:"template_type_dicts"}, axis=1)
        if(1 in self.df_template_type_dicts.columns):
            self.df_template_type_dicts  = self.df_template_type_dicts .rename({1:"template_type_dicts1"}, axis=1)
            self.df_template_type_dicts  = self.df_template_type_dicts .rename({2:"template_type_dicts2"}, axis=1)
            self.df_template_type_dicts  = self.df_template_type_dicts .rename({3:"template_type_dicts3"}, axis=1)
        if(4 in self.df_template_type_dicts.columns):
            self.df_template_type_dicts  = self.df_template_type_dicts .rename({4:"template_type_dicts4"}, axis=1)
            self.df_template_type_dicts  = self.df_template_type_dicts .rename({5:"template_type_dicts5"}, axis=1)
            self.df_template_type_dicts  = self.df_template_type_dicts .rename({6:"template_type_dicts6"}, axis=1)
        self.df=pd.concat([self.df_text,self.df_name_dicts,self.df_template_type_dicts], axis=1)
       
        # self.df = self.df.rename({1:"template_type_dicts1"}, axis=1)
        # self.df = self.df.rename({2:"template_type_dicts2"}, axis=1)
        # self.df = self.df.rename({3:"template_type_dicts3"}, axis=1)
        # self.df = self.df.rename({4:"template_type_dicts4"}, axis=1)
        self.df = self.df.fillna(0)
        self.df = self.df.reset_index()
        
        # if "template_type_dicts3" not in self.df.columns:
        #     self.df['template_type_dicts3'] = 0
        # if "template_type_dicts4" not in self.df.columns:
        #     self.df['template_type_dicts4'] = 0
            
        # if "template_type_dicts3" in self.df.columns:
        #     self.df["template_type_dicts3"]=0
        # if "template_type_dicts4" in self.df.columns:
        #     self.df["template_type_dicts4"]=0
        self.df1=self.df.loc[self.df['template_type_dicts'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df2=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df3=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df4=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df5=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        # self.df6=self.df.loc[self.df['template_type_dicts5'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        # self.df7=self.df.loc[self.df['template_type_dicts6'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df_1 = pd.concat([self.df1,self.df2,self.df3,self.df4,self.df5], ignore_index=True, sort=False)
        self.df6=self.df.loc[self.df['template_type_dicts'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df7=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df8=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df9=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df10=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        # self.df2=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df_2 = pd.concat([self.df6,self.df7,self.df8,self.df9,self.df10], ignore_index=True, sort=False)
       
        self.df11=self.df.loc[self.df['template_type_dicts'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df12=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df13=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df14=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df15=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        # self.df2=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df_3 = pd.concat([self.df11,self.df12,self.df13,self.df14,self.df15], ignore_index=True, sort=False)

        self.df16=self.df.loc[(self.df.template_type_dicts != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts != "http://purl.obolibrary.org/obo/PSDO_0000128")& (self.df.template_type_dicts != "http://purl.obolibrary.org/obo/PSDO_0000126")
        & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000128") & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000126")&
        (self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000129")&(self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000128")&(self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000126")&
        (self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000129")&(self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000128")&(self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000126")&
        (self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000129")&(self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000128")&(self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000126")]
        # self.df17=self.df.loc[(self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000128")& (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000126")
        # ]
        # self.df18=self.df.loc[(self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000128")& (self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000126")
        # ]
        # self.df19=self.df.loc[(self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000128")& (self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000126")
        # ]
        # self.df20=self.df.loc[(self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000128")& (self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000126")
        # ]
        # self.asd = pd.concat([self.df16,self.df17,self.df18,self.df19,self.df20], ignore_index=True, sort=False)
        # self.df12=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        # self.df13=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        # self.df14=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        # self.df15=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        
        
        # self.df16.to_csv("asd.csv")
        # self.df_1.to_csv("a129.csv")
        # self.df_2.to_csv("a128.csv")
        # self.df_3.to_csv("a126.csv")
        # self.df.to_csv("template.csv")
    
        return self.df,self.df_1,self.df_2,self.df_3,self.df16
   
    def create_candidates(self,df_spek,df_template):
        # df_template.to_csv("template_final.csv")
        # df_spek.to_csv("df_test.csv")
        # self.df_merged.to_csv("as.csv")
        count=0
        
        
        for rowIndex,row in df_template.iterrows():
            # print(row)
            for rowIndex1, row1 in df_spek.iterrows():
                # print(row1)
                # print(row1["comparator_type"])
                measure_name=row1["measure"]
                # oxcv=BNode(row1["Comparator_Node"][0])
                # print(row)
                # print(row1)
                oq=BNode()
                
        #print(row1)
                # ah=BNode(row1["Comparator_Node"])
                if "graph_type1" in df_spek.columns:
                    if (row1["graph_type1"] != 0):
                        count=count+1
                        # print(row1["graph_type1"])
                        ag=Literal(measure_name)
                        self.a.add((self.sq12,self.pq12,oq) )
                        self.a.add((oq,self.cp,self.co))
                        a25=Literal(row["text"])
                        a27=Literal(row["name"])
                        # a288= Literal(row["display"])
                        if "template_type_dicts" in df_template.columns:
                            if(row["template_type_dicts"] != 0):
                                a28=URIRef(row["template_type_dicts"])
                        if "template_type_dicts1" in df_template.columns:
                            if(row["template_type_dicts1"] != 0):
                                a29=URIRef(row["template_type_dicts1"])
                
                        self.a.add((oq,self.cp2,a25))
                        self.a.add((oq,self.cp1,a27))
                        # self.a.add((oq,self.cp3,a288))
                        # self.a.add((oq,self.cp3,a26))
                        # self.a.add((oq,self.cp3,a261))
                        self.a.add((oq,RDF.type,self.cp28))
                        if "template_type_dicts" in df_template.columns:
                            if(row["template_type_dicts"] != 0):
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a28))
                        if "template_type_dicts1" in df_template.columns:
                            if(row["template_type_dicts1"] != 0):
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a29))
                        if "template_type_dicts2" in df_template.columns:
                            if (row["template_type_dicts2"] != 0):
                                a30=URIRef(row["template_type_dicts2"])
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a30))
                        if "template_type_dicts3" in df_template.columns:
                            if (row["template_type_dicts3"] != 0):
                                a31=URIRef(row["template_type_dicts3"])
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a31))
                        if "template_type_dicts4" in df_template.columns:
                            if (row["template_type_dicts4"] != 0):
                                a32=URIRef(row["template_type_dicts4"])
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a32))
                        if "template_type_dicts5" in df_template.columns:
                            if (row["template_type_dicts5"] != 0):
                                a32=URIRef(row["template_type_dicts5"])
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a32))
                        if "template_type_dicts6" in df_template.columns:
                            if (row["template_type_dicts6"] != 0):
                                a32=URIRef(row["template_type_dicts6"])
                                ov=BNode()
                                self.a.add((oq,self.cop4,ov))
                                self.a.add((ov,RDF.type,a32))
                
                        idx=df_spek[df_spek["graph_type1"]==row1["graph_type1"]].index.values
                        row_list = df_spek.loc[idx, :].values.flatten().tolist()
                        # row_list = [item for item in row_list if not item.isdigit()]
                        row_list1=[]
                        for x in range(len(row_list)):
                            if type(row_list[x]) ==tuple:
                                row_list1.append(row_list[x])
                        Output = {}
                        for x, y in row_list1:
                            if y in Output:
                                Output[y].append(x)
                            else:
                                Output[y] = [x]
                        
                        # Printing Output
                        # print(str(Output))
                        for k,v in Output.items():
                            ov=BNode()
                            self.a.add((oq,self.cop4,ov))
                            a33=URIRef(k)
                            self.a.add((ov,RDF.type,a33))
                            for x in range(len(v)):
                                self.a.add((ov,self.cp23,v[x]))
                                #print(v[x])
                            self.a.add((ov,self.cp24,ag))
                        a35=BNode("-p1")
                        self.a.add((oq,self.cp26,a35))
                        self.a36=URIRef(row["index"])
                        self.a.add((oq,self.cp27,self.a36))
            # print(count)                
               
        return self.a
            





        
        
                




