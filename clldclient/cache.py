# coding: utf8
"""
To make clldclient reasonably performant and not too taxing on clld apps, we cache all
HTTP responses in a database. This module provides the database implementation.
"""
from __future__ import unicode_literals, print_function
import os
import datetime
import json
from collections import OrderedDict
import logging

from appdirs import user_cache_dir
from sqlalchemy import (
    Table, Column, Integer, DateTime, String, Binary, create_engine, MetaData, desc, and_,
)
from sqlalchemy.sql import select, functions
import requests
from purl import URL

import clldclient
from clldclient.link_header import get_links
from clldclient.util import graph, NO_DEFAULT


log = logging.getLogger(__name__)
metadata = MetaData()
responses = Table(
    'responses',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('created', DateTime, default=datetime.datetime.utcnow),
    Column('host', String(convert_unicode=True)),
    Column('request_url', String(convert_unicode=True)),  # the initially requested URL
    Column('accept', String(convert_unicode=True)),
    # the returned URL, potentially after following redirects
    Column('url', String(convert_unicode=True)),
    Column('headers', String(convert_unicode=True)),
    Column('content', Binary),
)


class Response(object):
    """Data of a response for an HTTP request to clld app.
    """
    def __init__(self, created, host, request_url, accept, url, headers, content):
        self.created = created
        self.request_url = request_url
        self.accept = accept
        self.url = url
        self.host = host
        self._content = content
        self.headers = {k.lower(): v for k, v in json.loads(headers).items()}

    @property
    def canonical_url(self):
        for link in self.links:
            if link['rel'] == 'canonical':
                return link['url']
        return self.url

    @property
    def content_type(self):
        return self.headers['content-type']

    @property
    def mimetype(self):
        return self.content_type.split(';')[0].strip()

    @property
    def links(self):
        return list(get_links(self.headers.get('link')))

    @property
    def content(self):
        if 'json' in self.content_type:
            return json.loads(self._content.decode('utf8'))
        if 'rdf+xml' in self.content_type:
            return graph(self._content)
        return self._content  # pragma: no cover


class Cache(object):
    def __init__(self):
        cache_dir = user_cache_dir(clldclient.__name__)
        self.path = os.path.join(cache_dir, 'db.sqlite')
        if not os.path.exists(cache_dir):
            try:
                os.makedirs(cache_dir)
            except OSError:  # pragma: no cover
                self.path = None
        self.db = self.init_db()

    def init_db(self):
        engine_url = 'sqlite://'
        if self.path:
            engine_url += '/%s' % self.path
        db = create_engine(engine_url)
        if not os.path.exists(self.path):
            metadata.create_all(db)
            log.info('db created at %s' % self.path)
        return db

    def get(self, url, default=NO_DEFAULT, headers=None):
        """Retrieve a Response object for a given URL.
        """
        headers = headers or {}
        url = URL(url)
        row = self.db.execute(
            select([
                responses.c.created,
                responses.c.host,
                responses.c.request_url,
                responses.c.accept,
                responses.c.url,
                responses.c.headers,
                responses.c.content])
            .where(and_(
                responses.c.request_url == url.as_string(),
                responses.c.accept == headers.get('Accept', '')))
        ).fetchone()
        if not row:
            log.info('cache miss %s' % url)
            row = self.add(url, headers)
            if row is None:
                if default is NO_DEFAULT:
                    raise KeyError(url)
                log.info('invalid url %s' % url)
                return default
        else:
            log.info('cache hit %s' % url)
        return Response(*row)

    def add(self, url, headers):
        response = requests.get(url.as_string(), headers=headers)
        if response.status_code == requests.codes.ok:
            values = OrderedDict()
            values['created'] = datetime.datetime.utcnow()
            values['host'] = url.host()
            values['request_url'] = url.as_string()
            values['accept'] = headers.get('Accept', '')
            values['url'] = response.url
            values['headers'] = json.dumps(dict(response.headers.items()))
            values['content'] = response.content
            self.db.execute(responses.insert().values(**values))
            return values.values()

    def drop(self):
        if self.path and os.path.exists(self.path):
            os.remove(self.path)
        self.db = self.init_db()

    def stats(self):
        """
        select host, count(pk), min(created), max(created) from responses group by host;
        """
        q = select([
            responses.c.host.label('host'),
            functions.count(responses.c.pk).label('amount'),
            functions.min(responses.c.created),
            functions.max(responses.c.created),
        ]).group_by('host').order_by(desc('amount'))
        return self.db.execute(q).fetchall()

    def purge(self, host=None, before=None, after=None):
        sql = responses.delete()
        if host:
            sql = sql.where(responses.c.host == host)
        if before:
            sql = sql.where(responses.c.created < before)
        if after:
            sql = sql.where(responses.c.created > after)
        res = self.db.execute(sql)
        log.info('%s rows deleted' % res.rowcount)
        return res.rowcount
