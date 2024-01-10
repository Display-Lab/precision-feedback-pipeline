
from rdflib import URIRef

def insert(merged_list,performer_graph,causal_pathways):
    id_name={}
    for sqe,pqe,oqe in causal_pathways.triples((None,URIRef("https://schema.metadatacenter.org/properties/4a88e066-a289-4a09-a0fc-a24c28c65215"),None)):
        id_name[sqe]=oqe
    p=URIRef("slowmo:acceptable_by")
    for x in merged_list:
        for z in x[0]:
           
            o=id_name[z]
            for i in x[1]:
                s=i
                performer_graph.add((s, p, o,))
    return performer_graph
