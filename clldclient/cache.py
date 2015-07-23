# coding: utf8
from __future__ import unicode_literals, print_function
import os
import datetime
import json
import logging
log = logging.getLogger(__name__)

from appdirs import user_cache_dir
from sqlalchemy import (
    Table, Column, Integer, DateTime, String, Binary, create_engine, MetaData,
)
from sqlalchemy.sql import select
import requests
import rdflib

import clldclient


metadata = MetaData()


resources = Table(
    'resources',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('created', DateTime, default=datetime.datetime.utcnow),
    Column('url', String),
    Column('content_type', String),
    Column('content', Binary),
)


class NoDefault(object):
    pass

NO_DEFAULT = NoDefault()


class Resource(object):
    def __init__(self, created, url, content_type, content):
        self.created = created
        self.url = url
        self._content = content
        self.content_type = content_type

    @property
    def content(self):
        if 'json' in self.content_type:
            return json.loads(self._content)
        if 'rdf+xml' in self.content_type:
            g = rdflib.Graph()
            return g.parse(data=self._content, format='xml')
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

    def get(self, url, default=NO_DEFAULT):
        row = self.db.execute(
            select([
                resources.c.created,
                resources.c.url,
                resources.c.content_type,
                resources.c.content])
            .where(resources.c.url == url)).fetchone()
        if not row:
            log.info('cache miss %s' % url)
            row = self.add(url)
            if row is None:
                if default is NO_DEFAULT:
                    raise KeyError(url)
                log.info('invalid url %s' % url)
                return default
        else:
            log.info('cache hit %s' % url)
        return Resource(*row)

    def add(self, url):
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            now = datetime.datetime.utcnow()
            self.db.execute(resources.insert().values(
                created=now,
                url=url,
                content_type=response.headers['content-type'],
                content=response.content))
            return now, url, response.headers['content-type'], response.content

    def drop(self):
        if self.path and os.path.exists(self.path):
            os.remove(self.path)
        self.db = self.init_db()
