import warnings
import time
import logging

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.serializer import Serializer
from rdfpandas.graph import to_dataframe
from SPARQLWrapper import XML, SPARQLWrapper

warnings.filterwarnings("ignore")


def read(file):
    #start_time = time.time()
    g = Graph()
    g.parse(data=file,format="json-ld")
    #logging.critical(" reading graph--- %s seconds ---" % (time.time() - start_time)) 
    return g

def process_causalpathways(causal_pathways):
    start_time = time.time()
    causal_dicts={}
    caus_type_dicts={}
    caus_out_dict={}
    caus_p = URIRef("http://schema.org/name")
    precdn=URIRef("http://purl.bioontology.org/ontology/SNOMEDCT/has_precondition")
    caus_s=[]
    for s, p, o in causal_pathways.triples((None,  caus_p, None)):
        # print(s)
        caus_s.append(s)
    for x in range(len(caus_s)):
        s=caus_s[x]
        p=precdn
        for s,p,o in causal_pathways.triples( (s, p, None) ):
            causal_dicts[o]=s
    ids= list(causal_dicts.values())
    ids = [*set(ids)]
    types=[]
    for x in range(len(ids)):
        y=[k for k,v in causal_dicts.items() if v == ids[x] ]  
        for i in range(len(y)):
            s=y[i]
            for s,p,o in causal_pathways.triples((s,RDF.type,None)):
                y[i]=o
        caus_type_dicts[ids[x]]=y        
    return caus_type_dicts

def process_spek(spek_cs):

    spek_out_dicts={}
    comparator_dicts={}
    #s=URIRef("http://example.com/app#mpog-aspire") 
    s=URIRef("http://example.com/app#display-lab")
    p=URIRef("http://example.com/slowmo#HasCandidate")
    gap_comparator=[URIRef('http://purl.obolibrary.org/obo/PSDO_0000104'),URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')]
    p1=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
    p2=URIRef("http://example.com/slowmo#RegardingComparator")

    i=0
    for s,p,o in spek_cs.triples( (s, p, None) ):
        s1= o
        BL=[]
        y=[o for s,p,o in spek_cs.triples((s1,p1,None))]
        for i in range(len(y)):
            # print(y[i])
            s=y[i]

            for s,p,o in spek_cs.triples((s,RDF.type,None)):
                
                y[i]=o
                
                if o in gap_comparator:
                    
                    for s,p,o in spek_cs.triples((s,p2,None)):
                        s=o
                        for s,p,o in spek_cs.triples((s,RDF.type,None)):
                            # print(o)
                            BL.append(o)
        
        spek_out_dicts[s1] = y
        comparator_dicts[s1]=BL
    # for k,v in comparator_dicts.items():
    #     print(k,v)
    return spek_out_dicts,comparator_dicts

def matching(caus_out_dict,spek_out_dicts,comparator_dicts):
    final_dict={}
    fg=list(caus_out_dict.values())
    fr=list(spek_out_dicts.values())
    fz=list(comparator_dicts.values())
    accept_ids=[]
    bnodes=[]
    

    
    for i in range(len(fg)):
        for x in range(len (fr)):
            result =  all(elem in fr[x]  for elem in fg[i])
            # print(result)
            if result == True:
                for a in range(len(fz)):

                    result1 = any(elem in fr[x]  for elem in fz[a])
                    if result1 == True:
                        l=[k for k,v in spek_out_dicts.items() if v == fr[x]]
                        bnodes.append(l)
                        y=[k for k,v in caus_out_dict.items() if v == fg[i]]
                        accept_ids.append(y)
                
    merged_list = [(accept_ids[i], bnodes[i]) for i in range(0, len(accept_ids))]
    return merged_list