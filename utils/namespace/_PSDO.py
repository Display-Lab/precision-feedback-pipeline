from rdflib import Namespace, URIRef

from utils.namespace import AliasingDefinedNamespace


class PSDO(AliasingDefinedNamespace):
    _NS = Namespace("http://purl.obolibrary.org/obo/")

    PSDO_0000002: URIRef
    performance_summary_display_template: URIRef

    PSDO_0000045: URIRef
    social_comparator_element: URIRef

    PSDO_0000093: URIRef
    comparator_content: URIRef

    # http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
    PSDO_0000094: URIRef
    goal_comparator_content: URIRef

    PSDO_0000095: URIRef
    social_comparator_content: URIRef

    PSDO_0000099: URIRef
    positive_performance_trend_content: URIRef

    PSDO_0000100: URIRef
    negative_performance_trend_content: URIRef

    PSDO_0000101: URIRef
    performance_trend_content: URIRef

    PSDO_0000102: URIRef
    performance_measure_content: URIRef

    PSDO_0000104: URIRef
    positive_performance_gap_content: URIRef

    PSDO_0000105: URIRef
    negative_performance_gap_content: URIRef

    PSDO_0000106: URIRef
    performance_gap_content: URIRef

    PSDO_0000107: URIRef
    performance_content: URIRef

    PSDO_0000112: URIRef
    achievement_content: URIRef

    PSDO_0000113: URIRef
    loss_content: URIRef

    PSDO_0000116: URIRef
    negative_performance_gap_set: URIRef

    PSDO_0000120: URIRef
    positive_performance_trend_set: URIRef

    PSDO_0000126: URIRef
    peer_average_comparator: URIRef

    PSDO_0000128: URIRef
    peer_75th_percentile_benchmark: URIRef

    PSDO_0000129: URIRef
    peer_90th_percentile_benchmark: URIRef

    PSDO_0000200: URIRef
    # TODO: change to `motivating_information_content
    motivating_information: URIRef

    _alias = {
        "performance_summary_display_template": "PSDO_0000002",
        "social_comparator_element": "PSDO_0000045",
        "comparator_content": "PSDO_0000093",
        "goal_comparator_content": "PSDO_0000094",
        "social_comparator_content": "PSDO_0000095",
        "positive_performance_trend_content": "PSDO_0000099",
        "negative_performance_trend_content": "PSDO_0000100",
        "performance_trend_content": "PSDO_0000101",
        "performance_measure_content": "PSDO_0000102",
        "positive_performance_gap_content": "PSDO_0000104",
        "negative_performance_gap_content": "PSDO_0000105",
        "performance_gap_content": "PSDO_0000106",
        "performance_content": "PSDO_0000107",
        "achievement_content": "PSDO_0000112",
        "loss_content": "PSDO_0000113",
        "negative_performance_gap_set": "PSDO_0000116",
        "positive_performance_trend_set": "PSDO_0000120",
        "peer_average_comparator": "PSDO_0000126",
        "peer_75th_percentile_benchmark": "PSDO_0000128",
        "peer_90th_percentile_benchmark": "PSDO_0000129",
        "motivating_information": "PSDO_0000200",
    }
