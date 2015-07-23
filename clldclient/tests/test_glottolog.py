# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch

from clldclient.cache import Resource


RESPONSES = {
    '/resource/languoid/iso/deu.json': """\
{
    "child_dialect_count": 3,
    "child_family_count": 0,
    "child_language_count": 0,
    "classification": [
        {
            "id": "indo1319",
            "name": "Indo-European",
            "url": "http://glottolog.org/resource/languoid/id/indo1319"
        },
        {
            "id": "high1287",
            "name": "High Franconian",
            "url": "http://glottolog.org/resource/languoid/id/high1287"
        }
    ],
    "description": null,
    "family_pk": 104971,
    "father_pk": 105784,
    "hid": "deu",
    "id": "stan1295",
    "iso639-3": "deu",
    "jsondata": {
        "endangerment": null,
        "ethnologue": "http://www.ethnologue.com/language/deu",
        "languagelandscape": "http://languagelandscape.org/language/German",
        "med": {
            "doctype": "grammar",
            "id": "320516",
            "name": "Zifonun, Gisela",
            "pages": 2598,
            "year": 1997
        },
        "sources": [
            {
                "doctype": "grammar",
                "id": "320516",
                "name": "Zifonun, Gisela",
                "pages": 2598,
                "year": 1997
            }
        ]
    },
    "latitude": 48.649,
    "level": "language",
    "longitude": 12.4676,
    "macroareas": {
        "eurasia": "Eurasia"
    },
    "markup_description": null,
    "name": "Standard German",
    "pk": 37168,
    "status": "established"
}""",
    '/resource/languoid/id/indo1319.json': """\
{
    "child_dialect_count": 1360,
    "child_family_count": 285,
    "child_language_count": 583,
    "classification": [],
    "description": null,
    "family_pk": null,
    "father_pk": null,
    "hid": null,
    "id": "indo1319",
    "jsondata": {
        "hname": "Indo-European",
        "languagelandscape": "http://languagelandscape.org/language/Indo-European"
    },
    "latitude": null,
    "level": "family",
    "longitude": null,
    "macroareas": {
        "africa": "Africa",
        "australia": "Australia",
        "eurasia": "Eurasia",
        "northamerica": "North America",
        "pacific": "Papunesia",
        "southamerica": "South America"
    },
    "markup_description": null,
    "name": "Indo-European",
    "pk": 104971,
    "status": "established"
}""",
}


class Tests(TestCase):
    def test_Glottolog(self):
        from clldclient.glottolog import Glottolog

        class MockClient(object):
            def __init__(self, host):
                self.host = host

            def get(self, url, **kw):
                return Resource(
                    None, url, 'application/json', RESPONSES.get(url, '{}').encode('utf8')
                )

        with patch('clldclient.glottolog.Client', MockClient):
            gl = Glottolog()
            deu = gl.languoid('deu')
            self.assertEquals(deu.id, 'stan1295')
            self.assertEquals(deu.iso_code, 'deu')
            assert deu.level
            assert deu.latitude
            assert deu.longitude
            ie = deu.get_family(gl)
            self.assertEquals(ie.name, 'Indo-European')
