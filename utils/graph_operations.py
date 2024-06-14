import json
import warnings
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from loguru import logger
from rdflib import Graph

warnings.filterwarnings("ignore")


def manifest_to_graph(templates_local) -> Graph:
    with urlopen(templates_local) as f:
        manifest = json.loads(f.read().decode("utf-8"))

    g: Graph = Graph()
    for item in manifest:
        temp_graph = Graph()
        parsed_url = urlparse(item)
        if not parsed_url.scheme:
            item = urljoin(templates_local, item)

        with urlopen(item) as f:
            template = f.read().decode("utf-8")

        temp_graph = Graph().parse(data=template, format="json-ld")
        g += temp_graph

        logger.debug(f"Graphed file {item}")

    return g
