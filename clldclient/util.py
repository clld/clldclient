# coding: utf8
from __future__ import unicode_literals

from six import PY2, binary_type, text_type
from rdflib import Graph


class NoDefault(object):
    pass

NO_DEFAULT = NoDefault()


def graph(data, **kw):
    kw.setdefault('format', 'xml')
    g = Graph()
    return g.parse(data=data, **kw)


def b(s):
    return s if PY2 else \
        (binary_type(s, encoding='utf8') if isinstance(s, text_type) else s)
