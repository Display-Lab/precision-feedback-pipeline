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
    causal_dicts={}
    caus_type_dicts={}
    caus_type_dicts1={}
    caus_out_dict={}
    gap_comparator=[URIRef('http://purl.obolibrary.org/obo/PSDO_0000104'),URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')]
    caus_p = URIRef("http://schema.org/name")
    precdn=URIRef("http://purl.bioontology.org/ontology/SNOMEDCT/has_precondition")
    name=URIRef("https://schema.metadatacenter.org/properties/4a88e066-a289-4a09-a0fc-a24c28c65215")
    caus_s=[]
    caus_n=[]
    
    for s, p, o in causal_pathways.triples((None, caus_p, None)):
        # print(s)
        caus_s.append(s)
        for sqe,pqe,oqe in causal_pathways.triples((None,name,None)):
            caus_n.append(oqe)
    for x in range(len(caus_s)):
        s=caus_s[x]
        p=precdn
        for s,p,o in causal_pathways.triples( (s, p, None) ):
            causal_dicts[o]=caus_n[x]
    ids= list(causal_dicts.values())
    ids = [*set(ids)]
    types=[]
    for x in range(len(ids)):
        yw=[]
        for s,p,o in causal_pathways.triples((s, p,None)):
                # print(s)
            #print(o)
            yw.append(o)

            # print("\n")
           
            if s == ids[x]:
                caus_type_dicts1[ids[x]]=yw
                # print(*yw)
                yw=[]
        y=[k for k,v in causal_dicts.items() if v == ids[x] ]  
        for i in range(len(y)):
            s=y[i]
            
            for s,p,o in causal_pathways.triples((s,RDF.type,None)):
                y[i]=o
                
        caus_type_dicts[ids[x]]=y  
    for k,v in caus_type_dicts.items():
        # print(k,v)
        for x in range(len(v)):
            if v[x] in  gap_comparator:
                gap=v[x]
    # for x in range(len(caus_s)):
    #     print(caus_s[x])
            
    # for k,v in caus_type_dicts.items():print(k, v)            
    # print(caus_type_dicts)
    # print(gap)
    return caus_type_dicts,gap

def process_spek(spek_cs,gap):

    spek_out_dicts={}
    comparator_dicts={}
    gap_comparator_dicts={}
    comparator_list=[]
    
    #s=URIRef("http://example.com/app#mpog-aspire") 
    s=URIRef("http://example.com/app#display-lab")
    p=URIRef("http://example.com/slowmo#HasCandidate")
    pew1=URIRef("http://example.com/slowmo#RegardingComparator")
    p1=URIRef("http://purl.obolibrary.org/obo/RO_0000091")
    p2=URIRef("http://example.com/slowmo#RegardingComparator")
    gap_comparator=[URIRef('http://purl.obolibrary.org/obo/PSDO_0000104'),URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')]
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
                comparator_gap_types=[]
                if o in gap_comparator:
                    y[i]=o
                    al=[]
                    for sew,pew,oew in spek_cs.triples((s,pew1,None)):
                        #print(s)
                        #print(oew)
                        al.append(oew)
                        
                        # for sew2,pew2,oew2 in spek_cs.triples((sew1,RDF.type,None)):
                        #     comparator_list.append(oew2)
                    comparator_list=[]
                    for asd in range(len(al)):
                        sew2=al[asd]
                        for sew2,pew2,oew2 in spek_cs.triples((sew2,RDF.type,None)):
                            # print(al[asd])
                            comparator_list.append(oew2)

                    #print(*al)
                    # print(o)
                    comparator_gap_types.append(y[i])
                    comparator_gap_types.append(comparator_list)
                    
                    # print(y[i])
                    # print(*comparator_gap_types)
                    
                    gap_comparator_dicts[s]=comparator_gap_types
                
                # print("\n")
                if o == gap:
                    
                    for s,p,o in spek_cs.triples((s,p2,None)):
                        s=o
                        for s,p,o in spek_cs.triples((s,RDF.type,None)):
                            
                            BL.append(o)
        # print("\n")
        spek_out_dicts[s1] = y
        comparator_dicts[s1]=BL
        
    # for k,v in gap_comparator_dicts.items():
    #     print(k,v)
    # print(spek_out_dicts)
    # print(*comparator_dicts)
    return spek_out_dicts,comparator_dicts,gap_comparator_dicts

def matching(caus_out_dict,spek_out_dicts,comparator_dicts,gap_comparator_dicts):
    final_dict={}
    fg=list(caus_out_dict.values())
    fr=list(spek_out_dicts.values())
    fz=list(comparator_dicts.values())
    fd=list(gap_comparator_dicts.values())
    # for k,v in caus_out_dict.items():print(k, v)
    positive_gap_comparator=URIRef('http://purl.obolibrary.org/obo/PSDO_0000104')
    negative_gap_comparator=URIRef('http://purl.obolibrary.org/obo/PSDO_0000105')
    fs=[]
    fw=[]
    for fgd in range(len(fd)):
        for fgds in range(len(fd[fgd])):
            if fd[fgd][fgds]== negative_gap_comparator:
                # print(fd[fgd][fgds])
                fs.append(fd[fgd][fgds+1])
                # print(fd[fgd][fgds+1])
            if fd[fgd][fgds] == positive_gap_comparator:
                # print(fd[fgd][fgds])
                fw.append(fd[fgd][fgds+1])
                # print(fd[fgd][fgds+1])
   
    accept_ids=[]
    bnodes=[]
    ng_list=[]
    p_list=[]
    comparator_list=[URIRef('http://purl.obolibrary.org/obo/PSDO_0000128'),URIRef('http://purl.obolibrary.org/obo/PSDO_0000129'),URIRef('http://purl.obolibrary.org/obo/PSDO_0000126')]
    for swd in range(len(fs)):
        for swd1 in range(len(fs[swd])):
            ng_list.append(fs[swd][swd1])
    # print(*ng_list)
    for swd2 in range(len(fw)):
        for swd3 in range(len(fw[swd2])):
            p_list.append(fw[swd2][swd3])
    # print(*p_list)
    status_bit=False
    for i in range(len(fg)):
        for x in range(len (fr)):
            result =  all(elem in fr[x]  for elem in fg[i])
            if result == True:
                result1 = False
                if negative_gap_comparator in fg[i]:
                   for f in range(len(fr[x])):
                        if fr[x][f] in ng_list and status_bit is False:
                            aby = fr[x].count(fr[x][f])
                            if aby == 2:
                                result1=True
                            if result1 == True:
                                status_bit=True
                                l=[k for k,v in spek_out_dicts.items() if v == fr[x]]
                                bnodes.append(l)
                                y=[k for k,v in caus_out_dict.items() if v == fg[i]]
                                accept_ids.append(y)
                if positive_gap_comparator in fg[i]:
                    for f in range(len(fr[x])):
                        if fr[x][f] in p_list and status_bit is False:
                            aby = fr[x].count(fr[x][f])
                            if aby == 2:
                                result1=True
                            if result1 == True:
                                status_bit= True
                                l=[k for k,v in spek_out_dicts.items() if v == fr[x]]
                                bnodes.append(l)
                                y=[k for k,v in caus_out_dict.items() if v == fg[i]]
                                accept_ids.append(y)  
        status_bit=False 
    merged_list = [(accept_ids[i], bnodes[i]) for i in range(0, len(accept_ids))]
    return merged_list