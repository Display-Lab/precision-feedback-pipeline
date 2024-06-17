import json
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from loguru import logger
from rdflib import Graph


def manifest_to_graph(templates_local: str) -> Graph:
    g: Graph = Graph()
    try:
        with urlopen(templates_local) as f:
            manifest = json.loads(f.read().decode("utf-8"))

    except Exception as e:
        logger.error(f"Error loading manifest: {e}")
        return g  # Return an empty graph if the manifest cannot be loaded

    for item in manifest:
        try:
            parsed_url = urlparse(item)
            if not parsed_url.scheme:
                item = urljoin(templates_local, item)

            with urlopen(item) as f:
                template = f.read().decode("utf-8")

            temp_graph = Graph().parse(data=template, format="json-ld")
            g += temp_graph

            logger.debug(f"Graphed file {item}")
        except Exception as e:
            logger.error(f"Error processing item {item}: {e}")
            continue

    return g
