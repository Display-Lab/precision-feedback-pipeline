
from rdflib import URIRef

def insert(merged_list,performer_graph,causal_pathways):
    id_name={}
    measure_list=[]
    for sqe,pqe,oqe in causal_pathways.triples((None,URIRef("https://schema.metadatacenter.org/properties/4a88e066-a289-4a09-a0fc-a24c28c65215"),None)):
        id_name[sqe]=oqe
    p=URIRef("slowmo:acceptable_by")
    for x in merged_list:
        for z in x[0]:
            o=id_name[z]
            print(o)
            causal_p= str(o)
            for i in x[1]:
                s=i
                if causal_p == "Social better":
                    for s5,p5,o5 in performer_graph.triples((s,URIRef("http://purl.obolibrary.org/obo/RO_0000091"),None)):
                        for s7,p7,o7 in performer_graph.triples((o5,URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),None)):
                            if  o7==URIRef("http://purl.obolibrary.org/obo/PSDO_0000104"):
                                for s7,p7,o8 in performer_graph.triples((o5,URIRef("http://example.com/slowmo#RegardingMeasure"),None)):
                                    if o8 in measure_list:
                                        print("yes")
                                        
                                        for s7,p7,o9 in performer_graph.triples((o5,URIRef("http://example.com/slowmo#RegardingComparator"),None)):
                                            for s10,p10,o10 in performer_graph.triples((o9,URIRef("http://purl.org/dc/terms/title"),None)):
                                                title_name=str(o10)
                                                print(title_name)
                                                if title_name == "TOP_25":
                                                    continue
                                                else:
                                                    performer_graph.add((s, p, o,))
                                    else:
                                        performer_graph.add((s, p, o,))
                                    measure_list.append(o8)
                else:
                    performer_graph.add((s, p, o,))
    return performer_graph
