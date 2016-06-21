# coding: utf8
from __future__ import unicode_literals
import os
from unittest import TestCase
from tempfile import mktemp
import shutil
import datetime
import time

from httmock import all_requests, response, HTTMock
from mock import patch, Mock


@all_requests
def clld(url, request):
    res = {
        '/resource/languoid/id/stan1295.json': (
            '<http://glottolog.org/>; rel="canonical"; type="text/html"',
            'application/json',
            ('{"id": "stan1295", "name": "Standard German"}')),
        '/resource/languoid/id/stan1295.rdf': (
            '',
            'application/rdf+xml; charset=utf8',
            ("""\
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dcterms="http://purl.org/dc/terms/">
    <rdf:Description rdf:about="http://glottolog.org/resource/languoid/id/stan1295">
        <dcterms:isReferencedBy rdf:resource="http://glottolog.org/resource/reference/id/7242"/>
    </rdf:Description>
</rdf:RDF>
""")),
    }.get(url.path)
    if res is None:
        return response(404, 'not found', {}, None, 5, request)
    return response(
        200, res[2], {'content-type': res[1], 'link': res[0]}, None, 5, request)


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
                self.assertEqual(r1.content['id'], 'stan1295')
                self.assertEqual(r1.canonical_url, 'http://glottolog.org/')
                r2 = cache.get('http://glottolog.org/resource/languoid/id/stan1295.json')
                self.assertEqual(r1.created, r2.created)
                cache.drop()
                r2 = cache.get('http://glottolog.org/resource/languoid/id/stan1295.json')
                self.assertNotEqual(r1.created, r2.created)
                self.assertRaises(KeyError, cache.get, 'http://glottolog.org/unknown')
                self.assertEqual(cache.get('http://glottolog.org/unknown', default=1), 1)
                res = cache.get('http://glottolog.org/resource/languoid/id/stan1295.rdf')
                self.assertEqual(res.mimetype, 'application/rdf+xml')
                self.assertEqual(
                    res.canonical_url,
                    'http://glottolog.org/resource/languoid/id/stan1295.rdf')
                assert hasattr(res.content, 'triples')
                self.assertEqual(res.links, [])
                cached = {r[0]: r[1] for r in cache.stats()}['glottolog.org']
                self.assertEqual(cached, cache.purge(host='glottolog.org'))
                now = datetime.datetime.utcnow()
                time.sleep(0.2)
                cache.get('http://glottolog.org/resource/languoid/id/stan1295.json')
                self.assertEqual(0, cache.purge(before=now, host='glottolog.org'))
                self.assertEqual(1, cache.purge(after=now, host='glottolog.org'))
