# coding: utf8
from __future__ import unicode_literals
import re

from clldclient.client import Client


ISO_CODE_PATTERN = re.compile('[a-z]{3}$')


class Languoid(dict):
    @property
    def id(self):
        return self['id']

    @property
    def name(self):
        return self['name']

    def get_family(self, client):
        ancestors = self.get('classification')
        if ancestors:
            return client.languoid(ancestors[0]['id'])

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


class Glottolog(Client):
    __host__ = 'glottolog.org'

    def languoid(self, code):
        type = 'iso' if ISO_CODE_PATTERN.match(code) else 'id'
        return Languoid(
            self.get('/resource/languoid/{0}/{1}.json'.format(type, code)).content)
