from typing import List

from rdflib import RDF, BNode, Graph, URIRef
from rdflib.resource import Resource

from utils import PSDO


class Signal:
    signal_type: URIRef

    @classmethod
    def select(cls, motivating_informations: List[Resource]) -> List[Resource]:
        return list(
            filter(
                cls.is_rdf_type_of,
                motivating_informations,
            )
        )

    @staticmethod
    def moderators(mi: Resource) -> dict:
        base_mods = {"type": []}
        for trend_type in mi[RDF.type]:
            base_mods["type"].append(trend_type.identifier)

        return base_mods

    @classmethod
    def _resource(cls) -> Resource:
        # TODO: Refactor to allow optional list of tuples (p, o) to ba added to base node
        base = Graph().resource(BNode())
        base.add(RDF.type, PSDO.motivating_information)
        base.add(RDF.type, cls.signal_type)

        return base

    @classmethod
    def is_rdf_type_of(cls, mi: Resource) -> bool:
        return cls.signal_type in {t.identifier for t in mi[RDF.type]}
        # return mi.graph.resource(cls.signal_type) in mi[RDF.type]


from bitstomach2.signals._comparison import Comparison  # noqa: E402
from bitstomach2.signals._trend import Trend  # noqa: E402

__all__ = ["Comparison", "Trend"]

signal_map = {
    PSDO.performance_gap_content: Comparison,
    PSDO.performance_trend_content: Trend,
}
