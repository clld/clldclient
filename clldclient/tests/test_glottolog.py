# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch

from clldclient.tests.util import MockCache


class Cache(MockCache):
    __responses__ = {
        'http://glottolog.org/': """\
""",
        'http://glottolog.org/resource/languoid/id/stan1295': """\
<rdf:RDF {0}>
  <rdf:Description rdf:about="http://glottolog.org/resource/languoid/id/stan1295">
    <void:inDataset rdf:resource="http://glottolog.org/"/>
    <rdfs:label xml:lang="en">Standard German</rdfs:label>
    <skos:prefLabel xml:lang="en">Standard German</skos:prefLabel>
    <skos:scopeNote xml:lang="x-clld">language</skos:scopeNote>
    <dcterms:title xml:lang="en">Standard German</dcterms:title>
    <geo:long rdf:datatype="http://www.w3.org/2001/XMLSchema#float">12.4676</geo:long>
    <geo:lat rdf:datatype="http://www.w3.org/2001/XMLSchema#float">48.649</geo:lat>
    <rdf:type rdf:resource="http://purl.org/dc/terms/LinguisticSystem"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/resource/reference/id/17282"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/resource/reference/id/8593"/>
    <lexvo:iso639P3PCode rdf:datatype="http://www.w3.org/2001/XMLSchema#string">deu</lexvo:iso639P3PCode>
    <owl:sameAs rdf:resource="http://dbpedia.org/resource/ISO_639:deu"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/valuesets/sc37168"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/valuesets/fc37168"/>
    <dcterms:spatial>Eurasia</dcterms:spatial>
    <skos:narrower rdf:resource="http://glottolog.org/resource/languoid/id/berl1235"/>
    <dcterms:spatial rdf:resource="http://www.geonames.org/countries/DE/"/>
    <skos:editorialNote>established</skos:editorialNote>
    <skos:broaderTransitive rdf:resource="http://glottolog.org/resource/languoid/id/indo1319"/>
    <rdf:type rdf:resource="http://purl.org/linguistics/gold/Language"/>
    <skos:broader rdf:resource="http://glottolog.org/resource/languoid/id/indo1319"/>
  </rdf:Description>
</rdf:RDF>""",
        'http://glottolog.org/resource/languoid/id/berl1235': """\
<rdf:RDF {0}>
  <rdf:Description rdf:about="http://glottolog.org/resource/languoid/id/stan1295">
    <void:inDataset rdf:resource="http://glottolog.org/"/>
    <rdfs:label xml:lang="en">...</rdfs:label>
    <skos:prefLabel xml:lang="en">...</skos:prefLabel>
    <skos:scopeNote xml:lang="x-clld">language</skos:scopeNote>
    <dcterms:title xml:lang="en">...</dcterms:title>
    <rdf:type rdf:resource="http://purl.org/dc/terms/LinguisticSystem"/>
    <skos:broaderTransitive rdf:resource="http://glottolog.org/resource/languoid/id/indo1319"/>
    <rdf:type rdf:resource="http://purl.org/linguistics/gold/Language"/>
    <skos:broader rdf:resource="http://glottolog.org/resource/languoid/id/stan1295"/>
  </rdf:Description>
</rdf:RDF>""",
        'http://glottolog.org/resource/languoid/id/indo1319': """
<rdf:RDF {0}>
    <rdf:Description rdf:about="http://glottolog.org/resource/languoid/id/indo1319">
        <void:inDataset rdf:resource="http://glottolog.org/"/>
        <rdfs:label xml:lang="en">Indo-European</rdfs:label>
        <skos:prefLabel xml:lang="en">Indo-European</skos:prefLabel>
            <skos:scopeNote xml:lang="x-clld">language</skos:scopeNote>
        <dcterms:title xml:lang="en">Indo-European</dcterms:title>
    <rdf:type rdf:resource="http://purl.org/dc/terms/LinguisticSystem"/>
  </rdf:Description>
</rdf:RDF>""",
        'http://glottolog.org/resource/languoid/iso/deu': """\
<rdf:RDF {0}>
  <rdf:Description rdf:about="http://glottolog.org/resource/languoid/id/stan1295">
    <void:inDataset rdf:resource="http://glottolog.org/"/>
    <rdfs:label xml:lang="en">Standard German</rdfs:label>
    <skos:prefLabel xml:lang="en">Standard German</skos:prefLabel>
    <skos:scopeNote xml:lang="x-clld">language</skos:scopeNote>
    <dcterms:title xml:lang="en">Standard German</dcterms:title>
    <geo:long rdf:datatype="http://www.w3.org/2001/XMLSchema#float">12.4676</geo:long>
    <geo:lat rdf:datatype="http://www.w3.org/2001/XMLSchema#float">48.649</geo:lat>
    <rdf:type rdf:resource="http://purl.org/dc/terms/LinguisticSystem"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/resource/reference/id/17282"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/resource/reference/id/8593"/>
    <lexvo:iso639P3PCode rdf:datatype="http://www.w3.org/2001/XMLSchema#string">deu</lexvo:iso639P3PCode>
    <owl:sameAs rdf:resource="http://dbpedia.org/resource/ISO_639:deu"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/valuesets/sc37168"/>
    <dcterms:isReferencedBy rdf:resource="http://glottolog.org/valuesets/fc37168"/>
    <dcterms:spatial>Eurasia</dcterms:spatial>
    <skos:narrower rdf:resource="http://glottolog.org/resource/languoid/id/berl1235"/>
    <skos:narrower rdf:resource="http://glottolog.org/resource/languoid/id/hann1239"/>
    <dcterms:spatial rdf:resource="http://www.geonames.org/countries/DE/"/>
    <skos:editorialNote>established</skos:editorialNote>
    <skos:narrower rdf:resource="http://glottolog.org/resource/languoid/id/mans1257"/>
    <skos:broaderTransitive rdf:resource="http://glottolog.org/resource/languoid/id/indo1319"/>
    <rdf:type rdf:resource="http://purl.org/linguistics/gold/Language"/>
    <skos:broader rdf:resource="http://glottolog.org/resource/languoid/id/indo1319"/>
  </rdf:Description>
</rdf:RDF>""",
    }


class Tests(TestCase):
    def test_Glottolog(self):
        from clldclient.glottolog import Glottolog

        with patch('clldclient.database.Cache', Cache):
            gl = Glottolog()
            gl.languoid('deu')
            deu = gl.languoid('http://glottolog.org/resource/languoid/id/stan1295')
            self.assertAlmostEquals(deu.longitude, 12.4676)
            assert deu.latitude
            self.assertEquals(deu.family.name, 'Indo-European')
            self.assertEquals(deu.parent.name, 'Indo-European')
            self.assertEquals(len(list(deu.children)), 1)
