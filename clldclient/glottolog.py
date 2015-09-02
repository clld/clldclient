# coding: utf8
from __future__ import unicode_literals
import re

from rdflib import URIRef, Literal

from clldclient.database import Database, Language


ISO_CODE_PATTERN = re.compile('[a-z]{3}$')


class Languoid(Language):
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

    @property
    def macroareas(self):
        return [l.value for l in self['dcterms:spatial'] if isinstance(l, Literal)]


class Glottolog(Database):
    def __init__(self):
        self.__resource_map__['language'] = Languoid
        Database.__init__(self, 'glottolog.org')

    def languoid(self, code):
        if ISO_CODE_PATTERN.match(code):
            code = URIRef(self.url('/resource/languoid/iso/{0}'.format(code)).as_string())
        return self.resource(code, 'language')
