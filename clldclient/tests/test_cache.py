# coding: utf8
from __future__ import unicode_literals
import os
from unittest import TestCase
from tempfile import mktemp
import shutil

from httmock import all_requests, response, HTTMock
from mock import patch, Mock


@all_requests
def clld(url, request):
    headers = {'content-type': 'application/json'}
    content = {
        '/resource/languoid/id/stan1295.json': {
            'id': 'stan1295', 'name': 'Standard German'}
    }.get(url.path)
    if content is None:
        return response(404, 'not found', {}, None, 5, request)
    return response(200, content, headers, None, 5, request)


class Tests(TestCase):
    def setUp(self):
        self.tmp = mktemp()

    def tearDown(self):
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp, ignore_errors=True)

    def test_Cache(self):
        from clldclient.cache import Cache

        with patch('clldclient.cache.user_cache_dir', Mock(return_value=self.tmp)):
            with HTTMock(clld):
                cache = Cache()
                r1 = cache.get('http://glottolog.org/resource/languoid/id/stan1295.json')
                self.assertEquals(r1.content['id'], 'stan1295')
                r2 = cache.get('http://glottolog.org/resource/languoid/id/stan1295.json')
                self.assertEquals(r1.created, r2.created)
                cache.drop()
                r2 = cache.get('http://glottolog.org/resource/languoid/id/stan1295.json')
                self.assertNotEquals(r1.created, r2.created)
                self.assertRaises(KeyError, cache.get, 'http://glottolog.org/unknown')
                self.assertEquals(cache.get('http://glottolog.org/unknown', default=1), 1)
