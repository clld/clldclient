# coding: utf8
"""
Functionality to access linguistic databases.

A database in this context means linguistic data published via a clld application.
"""
from __future__ import unicode_literals
import json
from collections import namedtuple

from rdflib import URIRef, Literal
from rdflib.namespace import VOID, SKOS, DCTERMS, RDFS, RDF
from purl import URL
from uritemplate import expand
from six import string_types

from clldclient.cache import Cache


NAMESPACES = dict(dcterms=DCTERMS, skos=SKOS, rdf=RDF, rdfs=RDFS, void=VOID)


class RdfResource(object):
    def __init__(self, res, client, rtype):
        self.type = rtype
        self.client = client
        assert res.mimetype == 'application/rdf+xml'
        self.uriref = URIRef(res.canonical_url)
        self.g = res.content

    @property
    def name(self):
        return self.get_text('rdfs:label')

    def __repr__(self):
        return '<%s type="%s" name="%s">' % (
            self.__class__.__name__, self.type, self.name)

    def __getitem__(self, item):
        if item.startswith('http:') or item.startswith('https:'):
            predicate = URIRef(item)
        elif ':' in item:
            prefix, localname = item.split(':', 1)
            predicate = NAMESPACES[prefix][localname]
        else:
            raise KeyError('%s' % item)
        return list(self.g.objects(self.uriref, predicate))

    def get_text(self, literals, language=None):
        if isinstance(literals, Literal):
            literals = [literals]
        elif isinstance(literals, string_types):
            literals = self[literals]
        for literal in literals:
            if language is None or language == literal.language:
                return '%s' % literal


class Index(RdfResource):
    @property
    def member_type(self):
        return self.get_text('skos:hiddenLabel', language='x-clld')

    @property
    def members(self):
        return self['skos:member']


class Dataset(RdfResource):
    @property
    def citation(self):
        return self.get_text('dcterms:bibliographicCitation')

    @property
    def license(self):
        return self.get_text('dcterms:license')

    @property
    def resource_types(self):
        res = []
        for s, p, o in self.g.triples((None, RDF.type, VOID['Dataset'])):
            if s != self.uriref:
                res.append(ResourceType(
                    s,
                    self.get_text(
                        self.g.objects(s, SKOS['hiddenLabel']), language='x-clld'),
                    self.get_text(self.g.objects(s, SKOS['prefLabel'])),
                    self.get_text(self.g.objects(s, SKOS['example']))))
        return {rt.name: rt for rt in res}


ResourceType = namedtuple('ResourceType', 'uriref name label uritemplate')


def get_resource_type(g, uriref):
    for literal in g.objects(uriref, SKOS['scopeNote']):
        if literal.language == 'x-clld':
            return '%s' % literal


class Database(object):
    """
    Interface to access a database published as clld app.

    >>> wals = Database('wals.info')
    """
    __resource_map__ = {'index': Index}

    def __init__(self, host):
        self.host = host
        self.cache = Cache()
        self._dataset = None

    @property
    def dataset(self):
        if self._dataset is None:
            self._dataset = Dataset(self.get(), self, 'dataset')
        return self._dataset

    def resource(self, id, type=None):
        if isinstance(id, string_types) and (id.startswith('/') or id.startswith('http')):
            id = URIRef(self.url(id).as_string())
        assert isinstance(id, URIRef) or type
        if not isinstance(id, URIRef):
            resource_type = self.dataset.resource_types[type]
            id = URIRef(expand(resource_type.uritemplate, dict(id=id)))
        res = self.get(id)
        rtype = get_resource_type(res.content, URIRef(res.canonical_url))
        cls = self.__resource_map__.get(rtype, RdfResource)
        return cls(res, self, rtype)

    def resources(self, type):
        if not isinstance(type, URIRef):
            type = self.dataset.resource_types[type].uriref
        return self.resource(type)

    def url(self, path='/', **query):
        url = URL(path)
        if not url.host():
            url = url.host(self.host)
        if not url.scheme():
            url = url.scheme('http')
        #if url.path_segment(-1):
        #    if ext and '.' not in url.path_segment(-1):
        #        url = url.path_segment(-1, '{0}.{1}'.format(url.path_segment(-1), ext))
        for k, v in query.items():
            url = url.query_param(k, v)
        return url

    def get(self, url='/', **query):
        _u = self.url(url, **query)
        if _u:
            return self.cache.get(
                self.url(url, **query).as_string(),
                default=None,
                headers={'Accept': 'application/rdf+xml'})

    #
    # FIXME: get list of resources and uri templates from void!
    #
    def get_datatables(self, url):  # pragma: no cover
        prefix = 'CLLD.DataTable.init('
        html = self.get(url).content.decode('utf8')
        for line in html.split('\n'):
            line = line.strip()
            if line.startswith(prefix):
                yield DataTable(json.loads('[%s]' % line[len(prefix):-2]))

    def formats(self, url):  # pragma: no cover
        for link in self.get(url).links:
            if link['rel'] == 'alternate':
                yield link


class DataTable(object):  # pragma: no cover
    def __init__(self, info):
        self.name = info[0]
        self.options = info[-1]
        self.base_url = URL(self.options['sAjaxSource'])
        self.cols = self.options['aoColumns']

    def url(self, sort=None, **kw):
        return
