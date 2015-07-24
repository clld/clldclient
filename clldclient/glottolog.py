# coding: utf8
from __future__ import unicode_literals
import re

import rdflib
from rdflib.namespace import DCTERMS

from clldclient.database import Database


ISO_CODE_PATTERN = re.compile('[a-z]{3}$')


class GlottologResource(dict):
    @property
    def id(self):
        return self['id']


class Languoid(GlottologResource):
    @property
    def name(self):
        return self['name']

    def get_family(self, client):
        ancestors = self.get('classification')
        if ancestors:
            return client.languoid(ancestors[0]['id'])

    def get_refs(self, client, limit=100):
        for ref in client.refs(self.id, limit=limit):
            yield ref

    @property
    def latitude(self):
        return self['latitude']

    @property
    def longitude(self):
        return self['longitude']

    @property
    def level(self):
        return self['level']

    @property
    def iso_code(self):
        return self.get('iso639-3')


class Glottolog(Database):
    def __init__(self):
        Database.__init__(self, 'glottolog.org')

    @staticmethod
    def resource_url(id, type):
        return 'http://glottolog.org/resource/{0}/id/{1}'.format(type, id)

    def languoid(self, code):
        type = 'iso' if ISO_CODE_PATTERN.match(code) else 'id'
        return Languoid(
            self.get('/resource/languoid/{0}/{1}.json'.format(type, code)).content)

    def refs(self, glottocode, limit=100):
        g = self.get('/resource/languoid/id/{0}.rdf'.format(glottocode))
        if g:
            for i, ref in enumerate(g.content.objects(
                    subject=rdflib.URIRef(self.resource_url(glottocode, 'languoid')),
                    predicate=DCTERMS['isReferencedBy'])):
                if i >= limit:
                    break
                yield GlottologResource(self.get('%s.json' % ref).content)
