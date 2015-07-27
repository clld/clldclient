# coding: utf8
"""
Functionality to access linguistic databases.

A database in this context means linguistic data published via a clld application.
"""
from __future__ import unicode_literals
import json

from rdflib import URIRef
from rdflib.namespace import VOID, SKOS, DCTERMS
from purl import URL
from uritemplate import expand

from clldclient.cache import Cache
from clldclient.util import NO_DEFAULT


class JsonResourceMap(dict):
    def __init__(self, d):
        super(JsonResourceMap, self).__init__({r['id']: r for r in d['resources']})
        self.uritemplate = d['properties']['uri_template']
        self.dataset = d['properties']['dataset']

    def url(self, rsc):
        if not isinstance(rsc, dict):
            if rsc not in self:
                return
            rsc = self[rsc]
        return expand(self.uritemplate, rsc)


class Subset(list):
    def __init__(self, g):
        self.type = g.label(None)
        super(Subset, self).__init__(g.objects(None, SKOS['member']))


class DataTable(object):
    def __init__(self, info):
        self.name = info[0]
        self.options = info[-1]
        self.base_url = URL(self.options['sAjaxSource'])
        self.cols = self.options['aoColumns']

    def url(self, sort=None, **kw):
        return


class Database(object):
    """
    Interface to access a database published as clld app.

    >>> wals = Database('wals.info')
    """
    def __init__(self, host):
        self.host = host
        self.cache = Cache()
        self._resourcemaps = {}

    @property
    def citation(self):
        return self.description().value(
            subject=self.uriref(), predicate=DCTERMS['bibliographicCitation'])

    @property
    def license(self):
        return self.description().value(
            subject=self.uriref(), predicate=DCTERMS['license'])

    def description(self, format=None):
        g = self.get('/void.rdf').content
        if format:
            return g.serialize(format=format)
        return g

    def subsets(self):
        return list(self.description().objects(self.uriref(), VOID['subset']))

    def subset(self, url):
        return Subset(self.get('%s.rdf' % url).content)

    def url(self, path='/', **query):
        url = URL(path)
        if not url.host():
            url = url.host(self.host)
        if not url.scheme():
            url = url.scheme('http')
        for k, v in query.items():
            url = url.query_param(k, v)
        return url

    def uriref(self, path='/', **query):
        return URIRef(self.url(path=path, **query).as_string())

    def get(self, url, default=NO_DEFAULT, **query):
        _u = self.url(url, **query)
        if _u:
            return self.cache.get(self.url(url, **query).as_string(), default=default)

    def get_datatables(self, url):
        prefix = 'CLLD.DataTable.init('
        html = self.get(url).content.decode('utf8')
        for line in html.split('\n'):
            line = line.strip()
            if line.startswith(prefix):
                yield DataTable(json.loads('[%s]' % line[len(prefix):-2]))

    def get_datatable(self):
        pass

    def formats(self, url):
        for link in self.get(url).links:
            if link['rel'] == 'alternate':
                yield link

    def resourcemap(self, rsc):
        if rsc not in self._resourcemaps:
            res = self.get('/resourcemap.json', rsc=rsc)
            if res:
                self._resourcemaps[rsc] = JsonResourceMap(res.content)
        return self._resourcemaps.get(rsc)

    def resource(self, rsc, id_, ext=None, type=None):
        rm = self.resourcemap(rsc)
        if rm:
            url = rm.url(id_)
            if url and (ext or type):
                for link in self.formats(url):
                    if (ext and link['ext'] == ext) or (type and link['type'] == type):
                        url = link['url']
                        break
            if url:
                return self.get(url)
