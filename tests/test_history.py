from typing import List

from rdflib import BNode, Graph, Literal, URIRef

from esteemer.signals import History


def test_history_detect_returns_list():
    message_history = {}

    signals = History.detect(message_history)
    assert not signals


def test_history_detect_signal():
    message_history = {}

    message_history["2023-06-01"] = {
        "template": "https://repo.metadatacenter.org/template-instances/1f257d98-f6b0-44f6-92c8-1a194954f33f",
        "causalpathway": "Social better",
    }

    message_history["2023-07-01"] = {
        "template": "different template B",
        "causalpathway": "Social worse",
    }
    message_history["2023-08-01"] = {
        "template": "https://repo.metadatacenter.org/template-instances/1f257d98-f6b0-44f6-92c8-1a194954f33f",
        "causalpathway": "Social better",
    }
    message_history["2023-09-01"] = {
        "template": "different template A",
        "causalpathway": "Social better",
    }
    message_history["current_month"] = {
        "template": "https://repo.metadatacenter.org/template-instances/1f257d98-f6b0-44f6-92c8-1a194954f33f",
        "causalpathway": "Social better",
    }

    signal = History.detect(message_history)[0]

    assert signal.value(URIRef("occurance")) == Literal(2)


def test_moderators_no_resources_return_empty_list():
    mods = History.moderators([])

    assert isinstance(mods, List)
    assert len(mods) == 0


def test_single_resource_returns_single_moderator():
    signal = Graph().resource(BNode())
    signal.add(URIRef("occurance"), Literal(4))
    mods = History.moderators([signal])

    assert isinstance(mods, List)
    assert isinstance(mods[0], dict)
    assert len(mods) == 1
    
    assert mods[0]["occurance"] == 4
