# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch

from clldclient.tests.util import MockCache


class Tests(TestCase):
    def test_Wals(self):
        from clldclient.wals import WALS

        with patch('clldclient.database.Cache', new=lambda: MockCache('wals_')):
            wals = WALS()
            lat = wals.language('lat')
            baltic = lat.genus
            self.assertIsNone(baltic.subfamily)
            self.assertEquals(baltic.family.name, 'Indo-European')
            self.assertEquals(baltic, wals.genus('baltic'))
            self.assertEquals(baltic.family, wals.family('indoeuropean'))
