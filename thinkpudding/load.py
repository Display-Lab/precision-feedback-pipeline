import warnings
import time

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

warnings.filterwarnings("ignore")


def read(file):
    #start_time = time.time()
    g = Graph()
    g.parse(data=file,format="json-ld")
    
    return g
#reading annotations from causal pathways
def process_causalpathways(causal_pathways):
    start_time = time.time()
    caus_type_dicts_final={}
    mod_type_dicts_final={}
    for s,p,o in causal_pathways.triples((None,URIRef("http://schema.org/name"),None)):
        # print(s)
        pre_list=[]
        mod_list=[]
        for s,p,o in causal_pathways.triples((s,URIRef("http://purl.bioontology.org/ontology/SNOMEDCT/has_precondition"),None)):
            pre_list.append(o)
        for s1,p1,o1 in causal_pathways.triples((s,URIRef("https://schema.metadatacenter.org/properties/c93ed038-0c67-4add-99c8-d1a0f1c0a864"),None)):
            # print(o1)
            mod_list.append(o1)
            
        caus_type_dicts_final[s]=pre_list
        mod_type_dicts_final[s]=mod_list
    
    
    return caus_type_dicts_final,mod_type_dicts_final

#reading annotation types from performer graph
def process_performer_graph(performer_graph):
    performer_graph_out_dicts={}
    i=0
    for s,p,o in performer_graph.triples( (URIRef("http://example.com/app#display-lab"), URIRef("http://example.com/slowmo#HasCandidate"), None) ):
        s1= o
        graph_type_list=[o for s,p,o in performer_graph.triples((s1,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),None))]
        for i in range(len(graph_type_list)):
            s=graph_type_list[i]
            for s,p,o in performer_graph.triples((s,RDF.type,None)):
                graph_type_list[i]=o
        performer_graph_out_dicts[s1] = graph_type_list
    return performer_graph_out_dicts

#matching the annotations from performer graph and causal_pathways
def matching(performer_graph_out_dicts,caus_out_dict_final):
    causal_pathway_types=list(caus_out_dict_final.values())
    performergraph_types=list(performer_graph_out_dicts.values())
    candidate_id_list=[]
    causal_pathway_id_list=[]
    combined_list=[]
   
    for i in range(len(causal_pathway_types)):
        for x in range(len (performergraph_types)):
            result =  all(elem in performergraph_types[x]  for elem in causal_pathway_types[i])
            if result == True :
                #candidate id
                l=[k for k,v in performer_graph_out_dicts.items() if v == performergraph_types[x]]
                #causal_pathway id
                y=[k for k,v in caus_out_dict_final.items() if v == causal_pathway_types[i]]
               
                candidate_id_list.append(y)
                causal_pathway_id_list.append(l)
               
    combined_list=[(candidate_id_list[i], causal_pathway_id_list[i]) for i in range(0, len(causal_pathway_id_list))]
    res = []
    [res.append(x) for x in combined_list if x not in res]
    
    return res