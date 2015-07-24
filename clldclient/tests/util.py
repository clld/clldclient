# coding: utf8
from __future__ import unicode_literals

from mock import MagicMock


class MockCache(object):
    __responses__ = {}

    def get(self, url, **kw):
        if url in self.__responses__:
            return MagicMock(content=self.__responses__[url])
