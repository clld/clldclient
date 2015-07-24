# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch

from clldclient.util import graph
from clldclient.tests.util import MockCache


class Cache(MockCache):
    __responses__ = {
        'http://wals.info/void.rdf': graph("""\
<rdf:RDF xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:void="http://rdfs.org/ns/void#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dcterms="http://purl.org/dc/terms/">
    <void:Dataset rdf:about="http://wals.info/">
        <rdfs:label xml:lang="en">WALS Online</rdfs:label>
        <dcterms:title xml:lang="en">WALS Online</dcterms:title>
        <dcterms:description xml:lang="en">The World Atlas of Language Structures Online</dcterms:description>
        <dcterms:license rdf:resource="http://creativecommons.org/licenses/by/4.0/"/>
        <void:subset rdf:resource="http://wals.info/chapter"/>
        <void:subset rdf:resource="http://wals.info/feature"/>
        <void:subset rdf:resource="http://wals.info/refdb"/>
        <dcterms:bibliographicCitation>
Dryer, Matthew S. &amp; Haspelmath, Martin (eds.) 2013.
The World Atlas of Language Structures Online.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at http://wals.info, Accessed on 2015-07-24.)
        </dcterms:bibliographicCitation>
    </void:Dataset>
</rdf:RDF>"""),
        'http://wals.info/chapter.rdf': graph("""\
<rdf:RDF xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:skos="http://www.w3.org/2004/02/skos/core#"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <skos:Collection rdf:about="http://wals.info/chapter">
        <rdfs:label xml:lang="en">contributions</rdfs:label>
        <skos:prefLabel xml:lang="en">contributions</skos:prefLabel>
        <skos:member rdf:resource="http://wals.info/chapter/13"/>
        <skos:member rdf:resource="http://wals.info/chapter/1"/>
        <skos:member rdf:resource="http://wals.info/chapter/2"/>
        <skos:member rdf:resource="http://wals.info/chapter/3"/>
        <skos:member rdf:resource="http://wals.info/chapter/4"/>
    </skos:Collection>
</rdf:RDF>"""),
}


class Tests(TestCase):
    def test_Database(self):
        from clldclient.database import Database

        with patch('clldclient.database.Cache', Cache):
            client = Database('wals.info')
            self.assertEquals(client.url('/p').as_string(), 'http://wals.info/p')
            self.assertEquals(client.url('/p', q='s').as_string(), 'http://wals.info/p?q=s')
            self.assertEquals(
                client.url('https://example.org/p').as_string(),
                'https://example.org/p')
            assert client.license
            assert client.citation
            assert client.subsets()
            self.assertEquals(len(client.subset('http://wals.info/chapter')), 5)

    def test_JsonResourceMap(self):
        from clldclient.database import JsonResourceMap

        rm = JsonResourceMap(dict(
            properties=dict(uri_template='http://example.org/{id}.json', dataset='ds'),
            resources=[dict(id='abc')]))
        self.assertEquals(rm.url('abc'), 'http://example.org/abc.json')
        self.assertIsNone(rm.url('xyz'))
