import warnings
import time

from rdflib import Graph, URIRef
from rdflib.namespace import RDF

warnings.filterwarnings("ignore")


def read(file):
    #start_time = time.time()
    g = Graph()
    g.parse(data=file,format="json-ld")
    #logging.critical(" reading graph--- %s seconds ---" % (time.time() - start_time)) 
    return g

def process_causalpathways(causal_pathways):
    start_time = time.time()
    
    caus_type_dicts_final={}
    
    caus_p = URIRef("http://schema.org/name")
    precdn=URIRef("http://purl.bioontology.org/ontology/SNOMEDCT/has_precondition")
    
    for s,p,o in causal_pathways.triples((None,caus_p,None)):
        # print(s)
        pre_list=[]
        for s,p,o in causal_pathways.triples((s,precdn,None)):
            pre_list.append(o)
            # print(o)
        # print(*pre_list)
        caus_type_dicts_final[s]=pre_list
    return caus_type_dicts_final

def process_spek(spek_cs):
    spek_out_dicts={}
    #s=URIRef("http://example.com/app#mpog-aspire") 
    s=URIRef("http://example.com/app#display-lab")
    p=URIRef("http://example.com/slowmo#HasCandidate")
    p1=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
    i=0
    a=[]
    for s,p,o in spek_cs.triples( (s, p, None) ):
        s1= o
        y=[o for s,p,o in spek_cs.triples((s1,p1,None))]
        # print(*y)
        for i in range(len(y)):
            s=y[i]
            for s,p,o in spek_cs.triples((s,RDF.type,None)):
                a.append(o)
                y[i]=o
        spek_out_dicts[s1] = y
    return spek_out_dicts

def matching(spek_out_dicts,caus_out_dict_final):
    fg=list(caus_out_dict_final.values())
    fr=list(spek_out_dicts.values())
    sjs=[]
    pjs=[]
    ysd=[]
   
    for i in range(len(fg)):
        for x in range(len (fr)):
            result =  all(elem in fr[x]  for elem in fg[i])
            if result == True :
                l=[k for k,v in spek_out_dicts.items() if v == fr[x]]
                # print(l)
                y=[k for k,v in caus_out_dict_final.items() if v == fg[i]]
                # print(y)
                sjs.append(y)
                pjs.append(l)
               
    ysd=[(sjs[i], pjs[i]) for i in range(0, len(pjs))]
    res = []
    [res.append(x) for x in ysd if x not in res]
    # print(*res)
    return res