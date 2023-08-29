
from rdflib import URIRef

def insert(merged_list,spek_cs,causal_pathways):
    caus_p = URIRef("http://schema.org/name")
    name=URIRef("https://schema.metadatacenter.org/properties/4a88e066-a289-4a09-a0fc-a24c28c65215")
    id_name={}
    
    # for s, p, o in causal_pathways.triples((None, caus_p, None)):
    #     print(s)
        # caus_s.append(s)
    for sqe,pqe,oqe in causal_pathways.triples((None,name,None)):
        # print(sqe)
        # print(oqe)
        id_name[sqe]=oqe
    # for k,v in id_name.items():
    #     print(k,v)
    p=URIRef("slowmo:acceptable_by")
    for x in merged_list:
        for z in x[0]:
           
            o=id_name[z]
            for i in x[1]:
                s=i
                spek_cs.add((s, p, o,))


    
   
    # for key, value in final_dict.items():
    #     print(list(key))
    #print(value)
        # for i in value:
        #     s=i
        #     o=[key]
        #     spek_cs.add((s, p, o,))
    return spek_cs
