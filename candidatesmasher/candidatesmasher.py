import warnings


import warnings


import pandas as pd
from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import RDF



warnings.filterwarnings("ignore", category=FutureWarning)
class CandidateSmasher:
    def __init__(self,performer_graph:Graph,templates:Graph):
        self.performer_graph=performer_graph
        self.templates=templates
        self.measure_dicts={}
        self.social_dicts={}
        self.goal_dicts={}
        self.graph_type_list=[]
        self.templates_list=[]
        self.peer_dicts={}
        self.top_10_dicts={}
        self.top_25_dicts={}
       

    def get_graph_type(self):
        for s,p,o in self.performer_graph.triples((URIRef("http://example.com/app#display-lab"), URIRef('http://example.com/slowmo#IsAboutMeasure'), None)):
            s1=o
            for s2,p2,o2 in self.performer_graph.triples((s1,URIRef("http://example.com/slowmo#WithComparator"),None)):
                self.measure_dicts[s1]=o2
                s3=o2
                
                for s4,p4,o4 in self.performer_graph.triples((s3,URIRef('http://schema.org/name'),None)):
                        #print(o4)
                        if str(o4)=="peers":
                            self.peer_dicts[s1]=o2
                        if str(o4)=="goal":
                            self.goal_dicts[s1]=o2
                        if str(o4)=="top_10":
                            self.top_10_dicts[s1]=o2
                        if str(o4)=="top_25":
                            self.top_25_dicts[s1]=o2
        #Accessing annotation types from peer comparator              
        peer_df = pd.DataFrame.from_dict(self.peer_dicts, orient ='index')
        peer_df= peer_df.reset_index()
        peer_df = peer_df.rename({"index":"measure"}, axis=1)
        peer_df = peer_df.rename({0:"Comparator_Node"}, axis=1)
        self.peer_types=[]
        for rowIndex, row in peer_df.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            peer_node_type=[]
            for  s81,p81,o81 in self.performer_graph.triples((None, None,o2)):
                for s82,p82,o82 in self.performer_graph.triples((s81,RDF.type,None)):
                    if s1 not in peer_node_type:
                        peer_node_type.append(s1)
                    if o2 not in peer_node_type:
                        peer_node_type.append(o2)
                    if str(o82) != "http://purl.obolibrary.org/obo/PSDO_0000102":
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        peer_node_type.append(node_tuple)
            peer_node_type_tuple=tuple(peer_node_type)
            peer_node_type_tuple=peer_node_type_tuple
            self.peer_types.append(peer_node_type_tuple)
       
        #Accessing annotation types from goal comparator        
        goal_df = pd.DataFrame.from_dict(self.goal_dicts, orient ='index')
        goal_df= goal_df.reset_index()
        goal_df = goal_df.rename({"index":"measure"}, axis=1)
        goal_df = goal_df.rename({0:"Comparator_Node"}, axis=1)
        self.goal_types=[]
        for rowIndex, row in goal_df.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            goal_node_type=[]
            for  s81,p81,o81 in self.performer_graph.triples((None, None,o2)):
                for s82,p82,o82 in self.performer_graph.triples((s81,RDF.type,None)):
                    if s1 not in goal_node_type:
                        goal_node_type.append(s1)
                    if o2 not in goal_node_type:
                        goal_node_type.append(o2)
                    if str(o82) != "http://purl.obolibrary.org/obo/PSDO_0000102":
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        goal_node_type.append(node_tuple)
            goal_node_type_tuple=tuple(goal_node_type)
            goal_node_type_tuple=goal_node_type_tuple
            self.goal_types.append(goal_node_type_tuple)
        
        #Accessing annotation types from top 10 comparator
        top_10_df = pd.DataFrame.from_dict(self.top_10_dicts, orient ='index')
        top_10_df= top_10_df.reset_index()
        top_10_df = top_10_df.rename({"index":"measure"}, axis=1)
        top_10_df = top_10_df.rename({0:"Comparator_Node"}, axis=1)
        self.top_10_types=[]
        for rowIndex, row in top_10_df.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            top_10_node_type=[]
            for  s81,p81,o81 in self.performer_graph.triples((None, None,o2)):
                for s82,p82,o82 in self.performer_graph.triples((s81,RDF.type,None)):
                    if s1 not in top_10_node_type:
                        top_10_node_type.append(s1)
                    if o2 not in top_10_node_type:
                        top_10_node_type.append(o2)
                    if str(o82) != "http://purl.obolibrary.org/obo/PSDO_0000102":
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        top_10_node_type.append(node_tuple)
                        
            top_10_node_type_tuple=tuple(top_10_node_type)
            top_10_node_type_tuple=top_10_node_type_tuple
            self.top_10_types.append(top_10_node_type_tuple)

        #Accessing annotation types from top25 comparator
        top25_df = pd.DataFrame.from_dict(self.top_25_dicts, orient ='index')
        top25_df= top25_df.reset_index()
        top25_df = top25_df.rename({"index":"measure"}, axis=1)
        top25_df = top25_df.rename({0:"Comparator_Node"}, axis=1)
        self.top_25_types=[]
        for rowIndex, row in top25_df.iterrows(): 
            s1=row["measure"]
            o2=row["Comparator_Node"]
            top_25_type=[]
            for  s81,p81,o81 in self.performer_graph.triples((None, None,o2)):
                for s82,p82,o82 in self.performer_graph.triples((s81,RDF.type,None)):
                    if s1 not in top_25_type:
                        top_25_type.append(s1)
                    if o2 not in top_25_type:
                        top_25_type.append(o2)
                    if str(o82) != "http://purl.obolibrary.org/obo/PSDO_0000102":
                        node=[]
                        node.append(o2)
                        node.append(str(o82))
                        node_tuple=tuple(node)
                        top_25_type.append(node_tuple)
            top_25_type_tuple=tuple(top_25_type)
            top_25_type_tuple=top_25_type_tuple
            self.top_25_types.append(top_25_type_tuple)
        
        #convert accessed goal,peer,top10,top25 to dataframes
        #convert peer types to dataframes    
        self.peer_types = pd.DataFrame(self.peer_types)
        self.goal_types=pd.DataFrame(self.goal_types)
        self.top_10_types=pd.DataFrame(self.top_10_types)
        self.top_25_types=pd.DataFrame(self.top_25_types)
        self.peer_types = self.peer_types.rename({0:"measure"}, axis=1)
        self.peer_types = self.peer_types.rename({1:"Comparator_Node1"}, axis=1)
        if 2 in self.peer_types:
            self.peer_types = self.peer_types.rename({2:"graph_type1"}, axis=1)
        if 3 in self.peer_types:
            self.peer_types = self.peer_types.rename({3:"graph_type2"}, axis=1)
        if 4 in self.peer_types:
            self.peer_types = self.peer_types.rename({4:"graph_type3"}, axis=1)
        if 5 in self.peer_types:
            self.peer_types = self.peer_types.rename({5:"graph_type4"}, axis=1)
        if 6 in self.peer_types:    
            self.peer_types = self.peer_types.rename({6:"graph_type5"}, axis=1)
        if 7 in self.peer_types:
            self.peer_types = self.peer_types.rename({7:"graph_type6"}, axis=1)
        self.peer_types = self.peer_types.fillna(0)
        self.peer_types["comparator_type"]="peers"
        self.peer_types=self.peer_types.reset_index(drop=True)
        self.peer_types = self.peer_types.drop('Comparator_Node1', axis=1)
      
        #convert goal types to dataframes 
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
        

        #convert top10 types to dataframes
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
       
        #convert top25 types to dataframes
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
       
        #merge all dataframes
        self.df_merged = pd.concat([self.goal_types,self.peer_types,self.top_10_types,self.top_25_types], ignore_index=True, sort=False)
        return self.df_merged,self.goal_types,self.peer_types,self.top_10_types,self.top_25_types

       

    def get_template_data(self):
        for sq,pq,oq in self.templates.triples((None,URIRef('http://schema.org/name'),None)):
            self.templates_list.append(str(sq))
        Text_dicts={}
        Name_dicts={}
        templatetype_dicts={}
        for x in range(len(self.templates_list)):
            template_node=URIRef(self.templates_list[x])
            isabout_type=[]
            for s30,p30,o30 in self.templates.triples((template_node,URIRef("https://schema.metadatacenter.org/properties/6b9dfdf9-9c8a-4d85-8684-a24bee4b85a8"),None)):
                Text_dicts[template_node]=str(o30)
            for s31,p31,o31 in self.templates.triples((template_node,URIRef("http://schema.org/name"),None)):
                Name_dicts[template_node]=str(o31)
            for s,p,o in self.templates.triples((template_node,URIRef("http://purl.obolibrary.org/obo/IAO_0000136"),None)):
                templatetype=str(o)
                isabout_type.append(templatetype)
            isabout_type_tuple=tuple(isabout_type)
            templatetype_dicts[template_node]=isabout_type_tuple
           
        text_dicts=Text_dicts
        name_dicts=Name_dicts
        template_type_dicts=templatetype_dicts
        
        self.df_text = pd.DataFrame.from_dict(text_dicts,orient='index')
        self.df_text = self.df_text.rename({0:"text"}, axis=1)
        
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
        self.df = self.df.fillna(0)
        self.df = self.df.reset_index()
        
        if "template_type_dicts3" not in self.df.columns:
            self.df['template_type_dicts3'] = 0
        if "template_type_dicts4" not in self.df.columns:
            self.df['template_type_dicts4'] = 0
            
        if "template_type_dicts3" in self.df.columns:
            self.df["template_type_dicts3"]=0
        if "template_type_dicts4" in self.df.columns:
            self.df["template_type_dicts4"]=0

        self.df1=self.df.loc[self.df['template_type_dicts'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df2=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df3=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df4=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df5=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000129"]
        self.df_1 = pd.concat([self.df1,self.df2,self.df3,self.df4,self.df5], ignore_index=True, sort=False)
        
        #Access all the annotations with peer average 
        self.df6=self.df.loc[self.df['template_type_dicts'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df7=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df8=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df9=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df10=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000128"]
        self.df_2 = pd.concat([self.df6,self.df7,self.df8,self.df9,self.df10], ignore_index=True, sort=False)
       
        #Access all the annotations with peer average       
        self.df11=self.df.loc[self.df['template_type_dicts'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df12=self.df.loc[self.df['template_type_dicts1'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df13=self.df.loc[self.df['template_type_dicts2'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df14=self.df.loc[self.df['template_type_dicts3'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df15=self.df.loc[self.df['template_type_dicts4'] == "http://purl.obolibrary.org/obo/PSDO_0000126"]
        self.df_3 = pd.concat([self.df11,self.df12,self.df13,self.df14,self.df15], ignore_index=True, sort=False)

        #Access all the annotations with top 10
        self.df16=self.df.loc[(self.df.template_type_dicts != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts != "http://purl.obolibrary.org/obo/PSDO_0000128")& (self.df.template_type_dicts != "http://purl.obolibrary.org/obo/PSDO_0000126")
        & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000129") & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000128") & (self.df.template_type_dicts1 != "http://purl.obolibrary.org/obo/PSDO_0000126")&
        (self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000129")&(self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000128")&(self.df.template_type_dicts2 != "http://purl.obolibrary.org/obo/PSDO_0000126")&
        (self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000129")&(self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000128")&(self.df.template_type_dicts3 != "http://purl.obolibrary.org/obo/PSDO_0000126")&
        (self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000129")&(self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000128")&(self.df.template_type_dicts4 != "http://purl.obolibrary.org/obo/PSDO_0000126")]
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
                measure: BNode = row1["measure"] 
                # oxcv=BNode(row1["Comparator_Node"][0])
                # print(row)
                # print(row1)
                candidate=BNode()
                
        #print(row1)
                # ah=BNode(row1["Comparator_Node"])
                if "graph_type1" in df_spek.columns:
                    if (row1["graph_type1"] != 0):
                        count=count+1
                        # print(row1["graph_type1"]) 
                        self.performer_graph.add((URIRef("http://example.com/app#display-lab"),URIRef("http://example.com/slowmo#HasCandidate"),candidate) )
                        self.performer_graph.add((candidate,RDF.type,URIRef("http://purl.obolibrary.org/obo/cpo_0000053")))
                        a25=Literal(row["text"])
                        a27=Literal(row["name"])
                        # a288= Literal(row["display"])
                        if "template_type_dicts" in df_template.columns:
                            if(row["template_type_dicts"] != 0):
                                a28=URIRef(row["template_type_dicts"])
                        if "template_type_dicts1" in df_template.columns:
                            if(row["template_type_dicts1"] != 0):
                                a29=URIRef(row["template_type_dicts1"])
                
                        self.performer_graph.add((candidate,URIRef("psdo:PerformanceSummaryTextualEntity"),a25))
                        self.performer_graph.add((candidate,URIRef("http://example.com/slowmo#name"),a27))
                        # self.a.add((oq,self.cp3,a288))
                        # self.a.add((oq,self.cp3,a26))
                        # self.a.add((oq,self.cp3,a261))
                        self.performer_graph.add((candidate,RDF.type,URIRef("http://example.com/slowmo#Candidate")))
                        self.performer_graph.add((candidate, URIRef("http://example.com/slowmo#RegardingMeasure"), measure))

                        if "template_type_dicts" in df_template.columns:
                            if(row["template_type_dicts"] != 0):
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a28))
                        if "template_type_dicts1" in df_template.columns:
                            if(row["template_type_dicts1"] != 0):
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a29))
                        if "template_type_dicts2" in df_template.columns:
                            if (row["template_type_dicts2"] != 0):
                                a30=URIRef(row["template_type_dicts2"])
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a30))
                        if "template_type_dicts3" in df_template.columns:
                            if (row["template_type_dicts3"] != 0):
                                a31=URIRef(row["template_type_dicts3"])
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a31))
                        if "template_type_dicts4" in df_template.columns:
                            if (row["template_type_dicts4"] != 0):
                                a32=URIRef(row["template_type_dicts4"])
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a32))
                        if "template_type_dicts5" in df_template.columns:
                            if (row["template_type_dicts5"] != 0):
                                a32=URIRef(row["template_type_dicts5"])
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a32))
                        if "template_type_dicts6" in df_template.columns:
                            if (row["template_type_dicts6"] != 0):
                                a32=URIRef(row["template_type_dicts6"])
                                ov=BNode()
                                self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                                self.performer_graph.add((ov,RDF.type,a32))
                
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
                            self.performer_graph.add((candidate,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),ov))
                            a33=URIRef(k)
                            self.performer_graph.add((ov,RDF.type,a33))
                            for x in range(len(v)):
                                self.performer_graph.add((ov,URIRef("http://example.com/slowmo#RegardingComparator"),v[x]))
                                #print(v[x])
                            self.performer_graph.add((ov,URIRef("http://example.com/slowmo#RegardingMeasure"),Literal(measure)))
                        a35=BNode("-p1")
                        self.performer_graph.add((candidate,URIRef("http://example.com/slowmo#AncestorPerformer"),a35))
                        self.a36=URIRef(row["index"])
                        self.performer_graph.add((candidate,URIRef("http://example.com/slowmo#AncestorTemplate"),self.a36))
        return self.performer_graph
            





        
        
                




