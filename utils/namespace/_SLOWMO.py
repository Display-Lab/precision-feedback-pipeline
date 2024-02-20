from rdflib import Namespace, URIRef

from utils.namespace import AliasingDefinedNamespace

class SLOWMO(AliasingDefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/")

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    SLOWMO_000123: URIRef  #
    SLOWMO_000124: URIRef  #
    SLOWMO_000125: URIRef  #

    # Aliases
    foo: URIRef
    # """SLOWMO_000123"""
    bar: URIRef
    # baz: URIRef

    _alias = {"foo": "SLOWMO_000123", "bar": "SLOWMO_000124"}

    _alias["baz"] = "SLOWMO_000125"
