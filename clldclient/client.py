# coding: utf8
from __future__ import unicode_literals

from purl import URL

from clldclient.cache import Cache


class Client(object):
    __host__ = None

    def __init__(self):
        self.cache = Cache()

    def get(self, url, **query):
        url = URL(url)
        if not url.host():
            url = url.host(self.__host__)
        if not url.scheme():
            url = url.scheme('http')
        for k, v in query.items():
            url = url.query_param(k, v)
        return self.cache.get(url.as_string())
