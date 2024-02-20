from rdflib import Namespace, URIRef

from utils.namespace import AliasingDefinedNamespace

class PSDO(AliasingDefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/")

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    PSDO_000123: URIRef  #
    PSDO_000124: URIRef  #
    PSDO_000125: URIRef  #

    # Aliases
    foo: URIRef
    # """PSDO_000123"""
    bar: URIRef
    # baz: URIRef

    _alias = {"foo": "PSDO_000123", "bar": "PSDO_000124"}

