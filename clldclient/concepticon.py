# coding: utf8
from __future__ import unicode_literals

from purl import URL

from clldclient.database import Database, Resource


class Concept(Resource):
    @property
    def concept_set(self):
        vs = self._get_first_resource('dcterms:isPartOf')
        return vs._get_first_resource('dcterms:isPartOf')


class Concepticon(Database):
    def __init__(self):
        self.__resource_map__['value'] = Concept
        Database.__init__(self, 'concepticon.clld.org')

    def search_concept(self, **query):
        return self.resource(
            URL('/search_concept').query_params(query).as_string(), 'value')
