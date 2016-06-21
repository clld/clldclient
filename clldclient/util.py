# coding: utf8
from __future__ import unicode_literals

from rdflib import Graph


class NoDefault(object):
    pass

NO_DEFAULT = NoDefault()


def graph(data, **kw):
    kw.setdefault('format', 'xml')
    g = Graph()
    return g.parse(data=data, **kw)
