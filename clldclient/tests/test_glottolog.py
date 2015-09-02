# coding: utf8
from __future__ import unicode_literals
from unittest import TestCase

from mock import patch

from clldclient.tests.util import MockCache


class Tests(TestCase):
    def test_Glottolog(self):
        from clldclient.glottolog import Glottolog

        with patch('clldclient.database.Cache', new=lambda: MockCache('glottolog_')):
            gl = Glottolog()
            gl.languoid('deu')
            deu = gl.languoid('http://glottolog.org/resource/languoid/id/stan1295')
            self.assertAlmostEquals(deu.longitude, 12.4676)
            assert deu.latitude
            self.assertEquals(deu.family.name, 'Indo-European')
            self.assertEquals(deu.parent.name, 'High Franconian')
            self.assertEquals(len(list(deu.children)), 3)
            self.assertEquals(deu.macroareas, ['Eurasia'])
