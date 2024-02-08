import time
import logging
#from asyncore import read


from thinkpudding.load import process_causalpathways, process_performer_graph, matching
from thinkpudding.insert import insert
class Thinkpudding:
    start_time1 = time.time()
    performer_graph_out_dicts = {}
    mod_type_dicts_final={}
    caus_out_dict={}
    final_dict={}
    
    def __init__(self, performer_graph, causal_pathways):
        start_time = time.time()
        self.performer_graph=performer_graph
        logging.critical(" reading spek graph--- %s seconds ---" % (time.time() - start_time)) 
        start_time = time.time()
        self.causal_pathways=causal_pathways
        logging.critical(" reading causal pathways graph--- %s seconds ---" % (time.time() - start_time))
    
    def process_causalpathways(self):
        start_time = time.time()
        self.caus_out_dict_final,self.mod_type_dicts_final=process_causalpathways(self.causal_pathways)
        logging.critical(" processing causal pathways--- %s seconds ---" % (time.time() - start_time))

    def process_performer_graph(self):
        start_time = time.time()
        self.performer_graph_out_dicts=process_performer_graph(self.performer_graph)
        logging.critical(" processing spek_cs--- %s seconds ---" % (time.time() - start_time))
    
    def matching(self):
        start_time = time.time()
        self.merged_list=matching(self.performer_graph_out_dicts,self.caus_out_dict_final)
        logging.critical(" processing matching--- %s seconds ---" % (time.time() - start_time))

    def insert(self):
        start_time = time.time()
        self.performer_graph_tp=insert(self.merged_list,self.performer_graph,self.causal_pathways,self.mod_type_dicts_final)
        logging.critical(" inserting acceptable by--- %s seconds ---" % (time.time() - start_time))
        return self.performer_graph_tp

