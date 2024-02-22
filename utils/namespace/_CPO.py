from rdflib import Namespace, URIRef

from utils.namespace import AliasingDefinedNamespace

class CPO(AliasingDefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/cpo/")

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    CPO_000123: URIRef  #
    CPO_000124: URIRef  #
    CPO_000125: URIRef  #

    # Aliases
    foo: URIRef
    # """CPO_000123"""
    bar: URIRef
    # baz: URIRef

    # _alias = {"foo": "CPO_000123", "bar": "CPO_000124"}

    # _alias["baz"] = "CPO_000125"
