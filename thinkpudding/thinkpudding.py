import time
import logging
#from asyncore import read


from thinkpudding.load import process_causalpathways, process_spek, matching
from thinkpudding.insert import insert
class Thinkpudding:
    start_time1 = time.time()
    spek_out_dicts = {}
    caus_out_dict={}
    final_dict={}
    
    def __init__(self, spek_cs, causal_pathways):
        start_time = time.time()
        #self.spek_cs1 = json.dumps(spek_cs)
        self.spek_cs=spek_cs
        logging.critical(" reading spek graph--- %s seconds ---" % (time.time() - start_time)) 
        start_time = time.time()
        #self.causal_pathways1 = json.dumps(causal_pathways)
        self.causal_pathways=causal_pathways
        logging.critical(" reading causal pathways graph--- %s seconds ---" % (time.time() - start_time))
    
    def process_causalpathways(self):
        start_time = time.time()
        
        self.caus_out_dict_final=process_causalpathways(self.causal_pathways)
        # for k,v in self.caus_out_dict.items():
        #     print(k,v)
        logging.critical(" processing causal pathways--- %s seconds ---" % (time.time() - start_time))

    def process_spek(self):
        start_time = time.time()
        self.spek_out_dicts=process_spek(self.spek_cs)
        logging.critical(" processing spek_cs--- %s seconds ---" % (time.time() - start_time))
    
    def matching(self):
        start_time = time.time()
        # matching(self.caus_out_dict,self.spek_out_dicts,self.comparator_dicts)
        self.merged_list=matching(self.spek_out_dicts,self.caus_out_dict_final)
        # for x in range(len(self.merged_list)):
        #     print(self.merged_list[x])

        logging.critical(" processing matching--- %s seconds ---" % (time.time() - start_time))

    def insert(self):
        start_time = time.time()
        self.spek_tp=insert(self.merged_list,self.spek_cs,self.causal_pathways)
        logging.critical(" inserting acceptable by--- %s seconds ---" % (time.time() - start_time))
        return self.spek_tp

# print(spek_tp.serialize(format='json-ld', indent=4))   
# logging.critical("complete thinkpudding--- %s seconds ---" % (time.time() - start_time1))
#print(caus_out_dict) 
#print(spek_out_dicts) 
#print(final_dict)          

