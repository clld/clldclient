# coding: utf8
from __future__ import unicode_literals
import os
from io import open

from purl import URL
from mock import MagicMock
import clldclient
from clldclient.util import graph


def get_resource(name, prefix):
    fname = os.path.join(
        os.path.dirname(clldclient.__file__),
        'tests',
        'resources',
        '{0}{1}.rdf'.format(prefix, name))
    if os.path.exists(fname):
        with open(fname, encoding='utf8') as fp:
            return graph(fp.read())


class MockCache(object):
    def __init__(self, prefix=''):
        self.prefix = prefix

    def get(self, url, **kw):
        url = URL(url)
        content = get_resource(
            url.path_segment(-1) if url.path_segments() else 'dataset', self.prefix)
        if content:
            return MagicMock(
                mimetype='application/rdf+xml',
                content=content,
                links=[dict(
                    url='{0}.html'.format(url.as_string),
                    ext='.html',
                    rel='alternate',
                    type='text/html')],
                canonical_url=url.as_string())
