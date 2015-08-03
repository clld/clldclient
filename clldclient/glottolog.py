# coding: utf8
from __future__ import unicode_literals
import re

from rdflib import URIRef

from clldclient.database import Database, Language


ISO_CODE_PATTERN = re.compile('[a-z]{3}$')


class Languoid(Language):
    def _get_first_resource(self, property_):
        urirefs = self[property_]
        if urirefs:
            return self.client.resource(urirefs[0])

    @property
    def parent(self):
        return self._get_first_resource('skos:broader')

    @property
    def family(self):
        return self._get_first_resource('skos:broaderTransitive')

    @property
    def children(self):
        for child in self['skos:narrower']:
            yield self.client.resource(child)


class Glottolog(Database):
    def __init__(self):
        self.__resource_map__['language'] = Languoid
        Database.__init__(self, 'glottolog.org')

    def languoid(self, code):
        if ISO_CODE_PATTERN.match(code):
            code = URIRef(self.url('/resource/languoid/iso/{0}'.format(code)).as_string())
        return self.resource(code, 'language')
