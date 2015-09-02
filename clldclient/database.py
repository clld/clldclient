# coding: utf8
"""
Functionality to access linguistic databases.

A database in this context means linguistic data published via a clld application.
"""
from __future__ import unicode_literals
import re
from collections import namedtuple

from rdflib import URIRef, Literal
from rdflib.namespace import VOID, SKOS, DCTERMS, RDFS, RDF, OWL, XSD, Namespace
from purl import URL
from uritemplate import expand
from six import string_types, text_type

from clldclient.cache import Cache
from clldclient.table import Table


GLOTTOLOG_LANGUOID_URI = re.compile(
    'http://glottolog.org/resource/languoid/id/(?P<glottocode>[a-z]{4}[0-9]{4})$')

NAMESPACES = dict(
    dcterms=DCTERMS,
    skos=SKOS,
    rdf=RDF,
    rdfs=RDFS,
    void=VOID,
    owl=OWL,
    lexvo=Namespace("http://lexvo.org/ontology#"),
    geo=Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
)


def get_first(iterable, filter_=None, attr=None):
    """helper to make dealing with generators as returned by `subjects` or `objects` easy.
    """
    for item in iterable:
        if filter_ is None or filter_(item):
            return getattr(item, attr) if attr else item


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
        return text_type('<{0} type="{1}" name="{2}">'.format(
            self.__class__.__name__, self.type, self.name).encode('ascii', 'replace'))

    def __eq__(self, other):
        if isinstance(other, RdfResource):
            return self.uriref == other.uriref
        return False

    def __getitem__(self, item):
        if item.startswith('http:') or item.startswith('https:'):
            predicate = URIRef(item)
        elif ':' in item:
            prefix, localname = item.split(':', 1)
            predicate = NAMESPACES[prefix][localname]
        else:
            raise KeyError('%s' % item)
        return list(self.g.objects(self.uriref, predicate))

    def _get_first(self, item, attr=None):
        return get_first(self[item], attr=attr)

    def get_text(self, literals, language=None):
        if isinstance(literals, Literal):
            literals = [literals]
        elif isinstance(literals, string_types):
            literals = self[literals]
        for literal in literals:
            if language is None or language == literal.language:
                return '%s' % literal

    def _get_first_resource(self, property_):
        urirefs = self[property_]
        if urirefs:
            return self.client.resource(urirefs[0])


class Index(RdfResource):
    @property
    def member_type(self):
        return self.get_text('skos:hiddenLabel', language='x-clld')

    @property
    def members(self):
        return self['skos:member']

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        for member in self.members:
            yield self.client.resource(member)


class Resource(RdfResource):
    @property
    def id(self):
        return self.get_text('skos:altLabel', language='x-clld')


class Language(Resource):
    @property
    def latitude(self):
        return self._get_first('geo:lat', attr='value')

    @property
    def longitude(self):
        return self._get_first('geo:long', attr='value')

    @property
    def iso_code(self):
        return self._get_first('lexvo:iso639P3PCode', attr='value')

    @property
    def glottocode(self):
        for uriref in self['owl:sameAs']:
            match = GLOTTOLOG_LANGUOID_URI.match(uriref)
            if match:
                return match.group('glottocode')


DomainElement = namedtuple('DomainElement', 'uriref name description number')


class Parameter(Resource):
    @property
    def domain(self):
        res = []
        for subject in self.g.subjects(SKOS['broader'], self.uriref):
            res.append(DomainElement(
                subject,
                get_first(self.g.objects(subject, DCTERMS['title']), attr='value'),
                get_first(
                    self.g.objects(subject, DCTERMS['description']),
                    filter_=lambda l: l.language == 'en',
                    attr='value'),
                get_first(
                    self.g.objects(subject, DCTERMS['description']),
                    filter_=lambda l: l.datatype == XSD.int,
                    attr='value'),
            ))
        return sorted(res, key=lambda de: de.number if de.number is not None else 0)


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
    __resource_map__ = {
        'index': Index,
        'language': Language,
        'parameter': Parameter,
    }

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
        cls = self.__resource_map__.get(rtype, Resource)
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

    def table(self, rsc, strip_html=True, **constraints):  # pragma: no cover
        return Table(rsc, self, strip_html=strip_html, **constraints)

    def formats(self, url):
        if isinstance(url, RdfResource):
            url = url.uriref
        for link in self.get(url).links:
            if link['rel'] == 'alternate':
                yield link
