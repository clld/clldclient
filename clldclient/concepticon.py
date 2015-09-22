# coding: utf8
from __future__ import unicode_literals

from purl import URL

from clldclient.database import Database, Resource


class Concept(Resource):
    @property
    def concept_set(self):
        vs = self._get_first_resource('dcterms:isPartOf')
        return vs._get_first_resource('dcterms:isPartOf')


class ConceptSet(Resource):
    @property
    def description(self):
        return self.get_text('dcterms:description')

    @property
    def ontological_category(self):
        return self.get_text('dcterms:type')

    @property
    def alt_labels(self):
        for uriref in self['dcterms:hasPart']:
            vs = self.client.resource(uriref)
            yield vs.get_text('dcterms:description', language='en')


class Concepticon(Database):
    def __init__(self):
        self.__resource_map__['parameter'] = ConceptSet
        self.__resource_map__['value'] = Concept
        Database.__init__(self, 'concepticon.clld.org')

    def search_concept(self, **query):
        return self.resource(
            URL('/search_concept').query_params(query).as_string(), 'value')
