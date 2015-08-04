# coding: utf8
from __future__ import unicode_literals
import argparse

from clldclient.database import Database


def download_table():
    parser = argparse.ArgumentParser(
        description="Download a table from a clld database",
        epilog="""\
This script can be used to download the content of dynamic tables displayed on
HTML pages of clld apps. The content is retrieved as a JSON array of objects,
and written to stdout, thus can be easily integrated into a pipeline of csvkit
commands.""")
    parser.add_argument('host', help='The database host, e.g. "wals.info"')
    parser.add_argument('resource', help='Resource type to download, e.g. "language"')
    parser.add_argument('--output', help='file path to write the data to', default=None)
    parser.add_argument(
        '--with-html',
        help="""By default, HTML markup is stripped from the data. Use this option to
keep it.""",
        action="store_true",
        default=False)

    constraints = ['parameter', 'language', 'contribution']
    for name in constraints:
        parser.add_argument(
            '--' + name,
            help="""\
"value" or "valueset" tables can often be restricted to a certain %s
by passing its local ID."""
                 % name,
            default=None)
    args = parser.parse_args()
    db = Database(args.host)
    table = db.table(
        args.resource,
        strip_html=not args.with_html,
        **{name: getattr(args, name) for name in constraints if getattr(args, name)})
    table.save(fname=args.output)
