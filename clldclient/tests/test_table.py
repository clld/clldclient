# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import Mock


class MockCache(object):
    def get(self, url, **kw):
        if url.as_string().endswith('.json'):
            content = {'columns': [{'sName': 'name'}]}
        else:
            content = {
                'iTotalDisplayRecords': 4, 'aaData': [['a name'], ['another name']]}
        return Mock(content=content)


class MockClient(object):
    dataset = Mock(resource_types={'language': Mock(uriref='/')})
    cache = MockCache()

    def url(self, path, *args, **kw):
        return path


class Tests(TestCase):
    def test_Table(self):
        from clldclient.table import Table

        Table('value', MockClient())
        t = Table('language', MockClient())
        t.sort(('name', 'desc'))
        t.sort()
        t.filter(name='a')
        t.filter()
        self.assertEquals(len(t), 4)
        self.assertEquals(len(list(t)), 4)
        assert t[0]
        assert t[1:4]
