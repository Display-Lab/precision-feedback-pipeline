import logging
import time
import warnings

from rdflib import Graph

warnings.filterwarnings("ignore")


def read_graph(file):
    start_time = time.time()
    g = Graph()
    g.parse(data=file, format="json-ld")

    logging.debug(" reading graph--- %s seconds ---" % (time.time() - start_time))
    return g


def create_base_graph(g1, g2, g3, g4):
    base_graph = g1 + g2 + g3 + g4  # merging graphs
    return base_graph
