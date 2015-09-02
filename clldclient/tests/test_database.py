# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch
from rdflib.namespace import DCTERMS

from clldclient.tests.util import MockCache


class Tests(TestCase):
    def test_Database(self):
        from clldclient.database import Database

        with patch('clldclient.database.Cache', MockCache):
            client = Database('localhost:6543')
            self.assertEquals(client.url('/p').as_string(), 'http://localhost:6543/p')
            self.assertEquals(
                client.url('/p', q='s').as_string(), 'http://localhost:6543/p?q=s')

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
            self.assertEquals(len(res), 1)
            for param in res:
                self.assertEquals(param.type, 'parameter')
            param = client.resource('parameter', 'parameter')
            self.assertEquals(len(param.domain), 2)
            self.assertEquals(param.id, 'parameter')
            param2 = client.resource('parameter', 'parameter')
            self.assertEquals(param, param2)
            self.assertFalse(param == 1)
            lat = client.resource('language', 'language')
            self.assertEquals(lat.iso_code, 'abc')
            self.assertEquals(lat.glottocode, 'abcd1234')
            self.assertEquals(len(list(client.formats(param))), 1)
