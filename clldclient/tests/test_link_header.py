# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase


class Tests(TestCase):
    def test_parse_links(self):
        from clldclient.link_header import get_links

        v = '</lect/wals_code_deu.html>; rel="alternate"; type="text/html", ' \
            '</lect/wals_code_deu.solr.json>; rel="alternate"; type="application/json", '\
            '</lect/wals_code_deu.json>; rel="alternate"; type="application/json", '\
            '</lect/wals_code_deu.nt>; rel="alternate"; type="text/nt"'
        links = list(get_links(v))
        self.assertEquals(len([l for l in links if l['ext'] == 'solr.json']), 1)
        self.assertEquals(len([l for l in links if l['type'] == 'application/json']), 2)
        self.assertEquals(list(get_links('')), [])
