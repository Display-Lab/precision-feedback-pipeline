
from rdflib import URIRef

def insert(merged_list,spek_cs):
    p=URIRef("slowmo:acceptable_by")
    for x in merged_list:
        for z in x[0]:
            o=z
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
