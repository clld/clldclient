# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch


class Tests(TestCase):
    def test_Client(self):
        from clldclient.client import Client

        class MockCache(object):
            def get(self, url, **kw):
                return url

        with patch('clldclient.client.Cache', MockCache):
            client = Client()
            client.__host__ = 'localhost'
            self.assertEquals(client.get('/p'), 'http://localhost/p')
            self.assertEquals(client.get('/p', q='s'), 'http://localhost/p?q=s')
            self.assertEquals(
                client.get('https://example.org/p'),
                'https://example.org/p')
