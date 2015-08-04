# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch
from rdflib.namespace import DCTERMS

from clldclient.tests.util import MockCache


class Cache(MockCache):
    __responses__ = {
        'http://wals.info/': """\
<rdf:RDF {0}>
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
    <void:Dataset rdf:about="http://wals.info/feature">
        <skos:prefLabel xml:lang="en">Features</skos:prefLabel>
        <skos:hiddenLabel xml:lang="x-clld">parameter</skos:hiddenLabel>
        <skos:example>http://wals.info/feature/{{id}}</skos:example>
        <void:rootResource rdf:resource="http://wals.info/feature"/>
    </void:Dataset>
    <void:Dataset rdf:about="http://wals.info/languoid">
        <skos:prefLabel xml:lang="en">Languages</skos:prefLabel>
        <skos:hiddenLabel xml:lang="x-clld">language</skos:hiddenLabel>
        <skos:example>http://wals.info/languoid/lect/wals_code_{{id}}</skos:example>
        <void:rootResource rdf:resource="http://wals.info/languoid"/>
    </void:Dataset>
</rdf:RDF>""",
        'http://wals.info/feature': """\
<rdf:RDF {0}>
    <skos:Collection rdf:about="http://wals.info/feature">
        <rdfs:label xml:lang="en">contributions</rdfs:label>
        <skos:prefLabel xml:lang="en">contributions</skos:prefLabel>
        <skos:scopeNote xml:lang="x-clld">index</skos:scopeNote>
        <skos:hiddenLabel xml:lang="x-clld">parameter</skos:hiddenLabel>
        <skos:member rdf:resource="http://wals.info/feature/13"/>
        <skos:member rdf:resource="http://wals.info/feature/1"/>
    </skos:Collection>
</rdf:RDF>""",
        'http://wals.info/feature/1': """\
<rdf:RDF {0}>
    <rdf:Description rdf:about="http://wals.info/feature/1">
        <rdfs:label xml:lang="en">Feature 1</rdfs:label>
        <skos:prefLabel xml:lang="en">Feature 1</skos:prefLabel>
        <skos:altLabel xml:lang="x-clld">1</skos:altLabel>
        <skos:scopeNote xml:lang="x-clld">parameter</skos:scopeNote>
    </rdf:Description>
    <rdf:Description rdf:about="http://wals.info/feature/1A#DE-1A-1">
        <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
        <rdfs:label xml:lang="en">Small</rdfs:label>
        <skos:prefLabel xml:lang="en">Small</skos:prefLabel>
        <dcterms:title xml:lang="en">Small</dcterms:title>
        <dcterms:description xml:lang="en">Small</dcterms:description>
        <skos:broader rdf:resource="http://wals.info/feature/1"/>
        <dcterms:description rdf:datatype="http://www.w3.org/2001/XMLSchema#int">1</dcterms:description>
    </rdf:Description>
    <rdf:Description rdf:about="http://wals.info/feature/1A#DE-1A-2">
        <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
        <rdfs:label xml:lang="en">Moderately small</rdfs:label>
        <skos:prefLabel xml:lang="en">Moderately small</skos:prefLabel>
        <dcterms:title xml:lang="en">Moderately small</dcterms:title>
        <dcterms:description xml:lang="en">Moderately small</dcterms:description>
        <skos:broader rdf:resource="http://wals.info/feature/1"/>
        <dcterms:description rdf:datatype="http://www.w3.org/2001/XMLSchema#int">2</dcterms:description>
    </rdf:Description>
</rdf:RDF>""",
        'http://wals.info/feature/13': """\
<rdf:RDF {0}>
    <rdf:Description rdf:about="http://wals.info/feature/13">
        <rdfs:label xml:lang="en">Feature 13</rdfs:label>
        <skos:prefLabel xml:lang="en">Feature 13</skos:prefLabel>
        <skos:altLabel xml:lang="x-clld">13</skos:altLabel>
        <skos:scopeNote xml:lang="x-clld">parameter</skos:scopeNote>
    </rdf:Description>
</rdf:RDF>""",
        'http://wals.info/languoid/lect/wals_code_lat': """\
<rdf:RDF {0}>
    <rdf:Description rdf:about="http://wals.info/languoid/lect/wals_code_lat">
        <void:inDataset rdf:resource="http://wals.info/"/>
        <rdfs:label xml:lang="en">Latvian</rdfs:label>
        <skos:prefLabel xml:lang="en">Latvian</skos:prefLabel>
        <skos:scopeNote xml:lang="x-clld">language</skos:scopeNote>
        <dcterms:title xml:lang="en">Latvian</dcterms:title>
        <geo:long rdf:datatype="http://www.w3.org/2001/XMLSchema#float">24.0</geo:long>
        <geo:lat rdf:datatype="http://www.w3.org/2001/XMLSchema#float">57.0</geo:lat>
        <dcterms:isReferencedBy rdf:resource="http://wals.info/refdb/record/Endzelin-1922"/>
        <dcterms:isReferencedBy rdf:resource="http://wals.info/refdb/record/Ekblom-1933"/>
        <lexvo:iso639P3PCode rdf:datatype="http://www.w3.org/2001/XMLSchema#string">lav</lexvo:iso639P3PCode>
        <owl:sameAs rdf:resource="http://dbpedia.org/resource/ISO_639:lav"/>
        <owl:sameAs rdf:resource="http://glottolog.org/resource/languoid/id/latv1249"/>
        <dcterms:isReferencedBy rdf:resource="http://wals.info/valuesets/144I-lat"/>
        <dcterms:isReferencedBy rdf:resource="http://wals.info/valuesets/144D-lat"/>
        <dcterms:spatial>Eurasia</dcterms:spatial>
        <skos:broader rdf:resource="http://wals.info/languoid/genus/baltic"/>
        <dcterms:spatial rdf:resource="http://www.geonames.org/countries/LV/"/>
    </rdf:Description>
</rdf:RDF>""",
    }


class Tests(TestCase):
    def test_Database(self):
        from clldclient.database import Database

        with patch('clldclient.database.Cache', Cache):
            client = Database('wals.info')
            self.assertEquals(client.url('/p').as_string(), 'http://wals.info/p')
            self.assertEquals(
                client.url('/p', q='s').as_string(), 'http://wals.info/p?q=s')

            ds = client.dataset
            assert ds.license
            assert ds.citation
            assert ds.name
            assert repr(ds)
            assert ds['http://purl.org/dc/terms/title']
            self.assertRaises(KeyError, ds.__getitem__, 'abcd')
            ds.get_text(list(ds.g.objects(ds.uriref, DCTERMS['title']))[0])
            self.assertEquals(len(ds.resource_types), 2)
            res = client.resources('parameter')
            self.assertEquals(res.member_type, 'parameter')
            self.assertEquals(len(res), 2)
            for param in res:
                self.assertEquals(param.type, 'parameter')
            param = client.resource('1', 'parameter')
            self.assertEquals(len(param.domain), 2)
            self.assertEquals(param.id, '1')
            param2 = client.resource('1', 'parameter')
            self.assertEquals(param, param2)
            self.assertFalse(param == 1)
            lat = client.resource('lat', 'language')
            self.assertEquals(lat.iso_code, 'lav')
            self.assertEquals(lat.glottocode, 'latv1249')
