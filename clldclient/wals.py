# coding: utf8
from __future__ import unicode_literals

from clldclient.database import Database, RdfResource


class Language(RdfResource):
    @property
    def genus(self):
        return self.client.resource(self['skos:broader'][0])


class Genus(RdfResource):
    @property
    def family(self):
        return self.client.resource(self['skos:broader'][0])

    @property
    def subfamily(self):
        return self.get_text('skos:hiddenLabel', language='en')

    @property
    def languages(self):
        return [self.client.resource(uri) for uri in self['skos:narrower']]


class Family(RdfResource):
    @property
    def genera(self):
        return [self.client.resource(uri) for uri in self['skos:narrower']]


class WALS(Database):
    def __init__(self):
        self.__resource_map__.update(
            language=Language,
            genus=Genus,
            family=Family)
        Database.__init__(self, 'wals.info')

    def language(self, code):
        return self.resource(code, 'language')

    def genus(self, id_):
        return self.resource(id_, 'genus')

    def family(self, id_):
        return self.resource(id_, 'family')
