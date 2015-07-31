# coding: utf8
"""
HTTP Link Header Parsing

Simple routines to parse and manipulate Link headers.

Adapted from
https://gist.githubusercontent.com/mnot/210535/raw/\
1755bb24a4f8796d55c280f1c50d0910f5522fb2/link_header.py
licensed as

Copyright (c) 2009 Mark Nottingham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import unicode_literals
import re

from purl import URL

TOKEN = r'(?:[^\(\)<>@,;:\\"/\[\]\?={} \t]+?)'
QUOTED_STRING = r'(?:"(?:\\"|[^"])*")'
PARAMETER = r'(?:%(TOKEN)s(?:=(?:%(TOKEN)s|%(QUOTED_STRING)s))?)' % locals()
LINK = r'<[^>]*>\s*(?:;\s*%(PARAMETER)s?\s*)*' % locals()
COMMA = r'(?:\s*(?:,\s*)+)'
LINK_SPLIT = r'%s(?=%s|\s*$)' % (LINK, COMMA)


def _unquotestring(instr):
    if instr[0] == instr[-1] == '"':
        instr = instr[1:-1]
        instr = re.sub(r'\\(.)', r'\1', instr)
    return instr


def _splitstring(instr, item, split):
    if not instr:
        return []  # pragma: no cover
    return [h.strip() for h in re.findall(r'%s(?=%s|\s*$)' % (item, split), instr)]

link_splitter = re.compile(LINK_SPLIT)


def get_links(instr):
    """
    Given a link-value, generate individual links as dict.
    """
    if instr:
        for link in [h.strip() for h in link_splitter.findall(instr)]:
            url, params = link.split(">", 1)
            url = URL(url[1:])
            fname = url.path_segments()[-1] if url.path_segments() else ''
            info = {
                'url': url.as_string(),
                'ext': fname.split('.', 1)[1] if '.' in fname else None,
                'rel': 'related',
                'type': 'application/octet-stream'}
            for param in _splitstring(params, PARAMETER, "\s*;\s*"):
                try:
                    a, v = param.split("=", 1)
                    info[a.lower()] = _unquotestring(v)
                except ValueError:  # pragma: no cover
                    info[param.lower()] = None
            yield info
