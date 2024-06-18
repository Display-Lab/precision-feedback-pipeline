from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

import yaml
from loguru import logger
from rdflib import Graph


def manifest_to_graph(manifest_path: str) -> Graph:
    g: Graph = Graph()
    
    try:
        manifest = extract_manifest(manifest_path)   
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

def extract_manifest(manifest_path: str) -> list:
    manifest = []
    with urlopen(manifest_path) as f:
        manifest_file = yaml.safe_load(f.read().decode("utf-8"))
        
    for key, values in manifest_file.items():
        parsed_url = urlparse(key)
        if not parsed_url.scheme:
            key = urljoin(manifest_path, key)
        for value in values:
            manifest.append(urljoin(key,value))
    return manifest
