# coding: utf8
from __future__ import unicode_literals

from mock import MagicMock
from clldclient.util import graph


class MockCache(object):
    __responses__ = {}
    __namespaces__ = """\
xmlns:foaf="http://xmlns.com/foaf/0.1/"
xmlns:owl="http://www.w3.org/2002/07/owl#"
xmlns:bibo="http://purl.org/ontology/bibo/"
xmlns:gold="http://purl.org/linguistics/gold/"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
xmlns:skos="http://www.w3.org/2004/02/skos/core#"
xmlns:void="http://rdfs.org/ns/void#"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:isbd="http://iflastandards.info/ns/isbd/elements/"
xmlns:frbr="http://purl.org/vocab/frbr/core#"
xmlns:dctype="http://purl.org/dc/dcmitype/"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
xmlns:dcterms="http://purl.org/dc/terms/"
xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
xmlns:vcard="http://www.w3.org/2001/vcard-rdf/3.0#"
xmlns:lexvo="http://lexvo.org/ontology#"\
"""

    def get(self, url, **kw):
        if url in self.__responses__:
            return MagicMock(
                mimetype='application/rdf+xml',
                content=graph(self.__responses__[url].format(self.__namespaces__)),
                canonical_url=url)
