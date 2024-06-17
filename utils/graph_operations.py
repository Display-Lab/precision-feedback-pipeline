import json
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from loguru import logger
from rdflib import Graph


def manifest_to_graph(manifest_path: str) -> Graph:
    g: Graph = Graph()
    try:
        with urlopen(manifest_path) as f:
            manifest = extract_paths(
                json.loads(f.read().decode("utf-8")), manifest_path
            )

    except Exception as e:
        logger.error(f"Error loading manifest: {e}")
        return g  # Return an empty graph if the manifest cannot be loaded

    for file in manifest:
        try:
            with urlopen(file) as f:
                file_content = f.read().decode("utf-8")

            temp_graph = Graph().parse(data=file_content, format="json-ld")
            g += temp_graph

            logger.debug(f"Graphed file {file}")
        except Exception as e:
            logger.error(f"Error processing item {file}: {e}")
            continue

    return g


def extract_paths(data, base_path=""):
    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            parsed_url = urlparse(key)
            if parsed_url.scheme:
                base_path = ""

            if isinstance(value, (list, dict)):
                # Recurse into the list or dict
                paths.extend(extract_paths(value, urljoin(base_path, key)))
            else:
                paths.append(urljoin(base_path, urljoin(key, value)))
    elif isinstance(data, list):
        for item in data:
            paths.extend(extract_paths(item, base_path))
    else:
        paths.append(urljoin(base_path, data))
    return paths
