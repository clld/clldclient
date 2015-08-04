# coding: utf8
from __future__ import unicode_literals
from collections import OrderedDict
from copy import copy
import json
from sys import stdout

from six import PY3, text_type
from bs4 import BeautifulSoup as bs
from purl import URL


class Table(object):
    def __init__(self, name, client, strip_html=True, **constraints):
        self.client = client
        self.name = name
        self.constraints = constraints
        if name in self.client.dataset.resource_types:
            self.base_url = '%s' % self.client.dataset.resource_types[name].uriref
        else:
            self.base_url = self.client.url('/%ss' % name)
        _cols = self.client.cache.get(
            URL('%s.json' % self.base_url).query_params(self.constraints),
            default=None)
        if _cols is None:
            raise ValueError(name)
        self.columns = OrderedDict()
        for spec in _cols.content['columns']:
            self.columns[spec['sName']] = spec
        self._params = {'sEcho': '1', 'iSortingCols': 0}
        self.strip_html = strip_html

    def sort(self, *args):
        if not args:
            self._params['iSortingCols'] = 0
            for k in list(self._params.keys()):
                if k.startswith('iSortCol_') or k.startswith('sSortDir_'):
                    del self._params[k]
            return

        n = self._params['iSortingCols']
        for spec in args:
            if isinstance(spec, (list, tuple)) and len(spec) == 2:
                col, dir_ = spec
            else:
                col, dir_ = spec, 'asc'
            self._params['iSortCol_%s' % (n)] = list(self.columns.keys()).index(col)
            self._params['sSortDir_%s' % (n)] = dir_
            n += 1
        self._params['iSortingCols'] = n

    def filter(self, **kw):
        if not kw:
            for k in list(self._params.keys()):
                if k.startswith('sSearch_'):
                    del self._params[k]
            return

        for col, term in kw.items():
            self._params['sSearch_%s' % list(self.columns.keys()).index(col)] = term

    def _get(self, **kw):
        params = copy(self._params)
        params.update(kw)
        params.update(self.constraints)
        res = self.client.cache.get(
            URL(self.base_url).query_params(params),
            headers={'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'})
        if res:
            return res.content['iTotalDisplayRecords'], res.content['aaData']

    def __len__(self):
        return self._get(iDisplayLength=1)[0]

    def __iter__(self):
        total, rows = self._get(iDisplayLength=1000)
        i = 0
        while total > i:
            for row in rows:
                i += 1
                yield self._to_dict(row)

            total, rows = self._get(iDisplayStart=i, iDisplayLength=1000)
            if not rows:
                raise StopIteration()

    def _to_dict(self, item):
        res = OrderedDict()
        for i, k in enumerate(self.columns.keys()):
            res[k] = item[i]
            if isinstance(res[k], text_type) and self.strip_html:
                res[k] = bs(res[k], "html5lib").get_text(strip=True)
        return res

    def __getitem__(self, item):
        if isinstance(item, slice):
            self._params['iDisplayStart'] = item.start or 0
            self._params['iDisplayLength'] = item.stop - item.start
        else:
            self._params['iDisplayStart'] = item
            self._params['iDisplayLength'] = 1
        _, res = self._get()
        if res:
            if isinstance(item, slice):
                items = []
                for i in range(0, len(res), item.step or 1):
                    items.append(self._to_dict(res[i]))
                return items
            return self._to_dict(res[0])
        if isinstance(item, slice):  # pragma: no cover
            return []
        raise KeyError(item)

    def save(self, fname=None):  # pragma: no cover
        if fname is None:
            stdout.write(json.dumps(list(self), indent=4))
            return
        _kw = dict(mode='w')
        if PY3:
            _kw['encoding'] = 'utf8'
        with open(fname, **_kw) as fp:
            return json.dump(list(self), fp)
