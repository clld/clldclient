# clldclient

<blockquote style="background-color: #fbe8e8; border-left: 5px solid #d9534f">
<strong>clldclient</strong> is deprecated. We are moving to a new model to access the data served by clld applications
based on <a href="http://cldf.clld.org">CLDF</a> as exchange format.
</blockquote>

Functionality to access the API of [clld](https://github.com/clld/clld) apps, e.g.
the databases published on the [CLLD](http://clld.org) platform.

[![Build Status](https://travis-ci.org/clld/clldclient.svg?branch=v1.0.1)](https://travis-ci.org/clld/clldclient)
[![codecov.io](http://codecov.io/github/clld/clldclient/coverage.svg?branch=master)](http://codecov.io/github/clld/clldclient?branch=master)
[![PyPI](https://img.shields.io/pypi/v/clldclient.svg)](https://pypi.python.org/pypi/clldclient)


## Installation

You can install from PyPI
```
pip install clldclient
```
or from a GitHub repository clone
```
git clone https://github.com/clld/clldclient.git
cd clldclient
python setup.py develop
```
The client library should work with python 2 >= 2.7 and python 3 >= 3.4.


## Usage

This client provides two orthogonal methods to access data in clld databases.

1. Functionality to access data from dynamic tables displayed within clld apps.
2. Functionality to navigate a database's resource graph programmatically.


### Accessing dynamic tabular data

clld apps often list resources using customized dynamic tables; e.g. the 
[WALS language table] adds *Genus*, *Family* and *Macroarea* columns. Accessing or
downloading this data is possible (by emulating what the browser does to retrieve the
table contents), but tedious and hampered by the fact that the data must often be 
downloaded in batches. This is made easy using `clldclient` functionality:

```python
>>> from clldclient.wals import WALS
>>> wals = WALS()
>>> languages = wals.table('language')
>>> list(languages.columns.keys())
[u'name', u'id', u'iso_codes', u'genus', u'family', u'macroarea', u'latitude', u'longitude', u'countries']
>>> languages[0]['name']
u'A-Pucikwar'
>>> languages.sort(('name', 'desc'))
>>> languages[0]['name']
u'Zuni'
>>> languages.filter(name='uni')
>>> len(languages)
10
>>> [l['name'] for l in languages[2:4]]
[u'Prasuni', u'Nuni (Northern)']
>>> languages.filter()  # calling filter without arguments resets all filters
>>> len(languages)
2679
>>> all = list(languages)  # languages is not a sequence, but provides an iterator
>>> len(all)  # now we downloaded all rows in several batches
2679
>>> all[1500]
OrderedDict([(u'name', u'Kokni'), (u'id', u'kkz'), (u'iso_codes', u'kex'), ...])
```

The basic functionality of downloading all rows of a dynamic table is also exposed as
command line script `clld-download-table`:

```
$ clld-download-table -h
usage: clld-download-table [-h] [--output OUTPUT] [--with-html]
                           [--parameter PARAMETER] [--language LANGUAGE]
                           [--contribution CONTRIBUTION]
                           host resource

Download a table from a clld database

positional arguments:
  host                  The database host, e.g. "wals.info"
  resource              Resource type to download, e.g. "language"

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       file path to write the data to
  --with-html           By default, HTML markup is stripped from the data. Use
                        this option to keep it.
  --parameter PARAMETER
                        "value" or "valueset" tables can often be restricted
                        to a certain parameter by passing its local ID.
  --language LANGUAGE   "value" or "valueset" tables can often be restricted
                        to a certain language by passing its local ID.
  --contribution CONTRIBUTION
                        "value" or "valueset" tables can often be restricted
                        to a certain contribution by passing its local ID.

This script can be used to download the content of dynamic tables displayed on
HTML pages of clld apps. The content is retrieved as a JSON array of objects,
and written to stdout, thus can be easily integrated into a pipeline of csvkit
commands.
```

As noted in the help message, the `clld-download-table` command can  easily be integrated
in a pipeline of UNIX-style commands like the ones provided by 
[csvkit](http://csvkit.readthedocs.org/en/latest/). Below we use 
[in2csv](http://csvkit.readthedocs.org/en/latest/scripts/in2csv.html) to convert our JSON
download to csv, and then get a quick overview of the data via
[csvstat](http://csvkit.readthedocs.org/en/latest/scripts/csvstat.html):

```
$ clld-download-table wals.info value --parameter 1A | in2csv -f json | csvstat
  1. language
	<type 'unicode'>
	Nulls: False
	Unique values: 563
	Max length: 32
  2. value
	<type 'unicode'>
	Nulls: False
	Values: Large, Small, Average, Moderately large, Moderately small
  3. source
	<type 'unicode'>
	Nulls: True
	Unique values: 557
	5 most frequent values:
		Tucker and Bryan 1966:	4
		McKaughan 1958;McKaughan and Macaraya 1967:	1
		Childs 1995:	1
		Heye and Hidalgo 1967;Cottle and Cottle 1958;Hidalgo and Hidalgo 1971:	1
		Kaufman 1971:	1
	Max length: 107
  4. m
	<type 'NoneType'>
	Nulls: True
	Values: 
  5. c
	<type 'NoneType'>
	Nulls: True
	Values: 

Row count: 563
```

Note that while you can use this functionality to download all of almost 270,000 
references from Glottolog, this will take some time and system resources, since the
whole JSON document must be constructed in memory before printing it to standard out:

```
$ time clld-download-table glottolog.org source | in2csv -f json > glottolog-refs.csv

real	89m5.502s
user	44m30.267s
sys	0m14.349s

$ du -sh glottolog-refs.csv 
30M	glottolog-refs.csv

$ du -sh ~/.cache/clldclient/db.sqlite 
178M	/home/robert/.cache/clldclient/db.sqlite
```

Also note that stripping HTML markup from the data incurs a big processing penalty - so
when speed is important, use the `--with-html` option.


### Navigating the resource graph of generic clld apps

You can access any clld database by passing the name of the host serving the app when
initializing a `Database` object:
```python
>>> from clldclient.database import Database
>>> apics = Database('apics-online.info')
>>> print(apics.dataset.citation)

Michaelis, Susanne Maria & Maurer, Philippe & Haspelmath, Martin & Huber, Magnus (eds.) 2013.
Atlas of Pidgin and Creole Language Structures Online.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at http://apics-online.info, Accessed on 2015-07-24.)

>>> assert 'language' in apics.dataset.resource_types
>>> languages = apics.resources('language')
>>> len(languages)
104
>>> for lang in languages:
...     print(lang)
...     break
...     
<Resource type="language" name="Tayo">
```

#### Bespoke database access

##### [Glottolog](http://glottolog.org)

The `Glottolog` client provides convenient access to the language classification:

```python
>>> from clldclient.glottolog import Glottolog
>>> glottolog = Glottolog()
>>> deu = glottolog.languoid('deu')
>>> deu2 = glottolog.languoid('stan1295')
>>> deu2 == deu
True
>>> deu.family
<Languoid type="language" name="Indo-European">
>>> for child in deu.family.children:
...     print(child)
...     break
...     
<Languoid type="language" name="Messapic">
```

##### [WALS](http://wals.info)

The `WALS` client provides access to the 
[WALS genealogy](http://wals.info/languoid/genealogy):

```python
>>> from clldclient.wals import WALS
>>> wals = WALS()
>>> l = wals.language('deu')
>>> l
<Language type="language" name="Deuri">
>>> l.genus
<Genus type="genus" name="Bodo-Garo">
>>> l.genus.family
<Family type="family" name="Sino-Tibetan">
>>> l.genus.languages[0]
<Language type="language" name="Garo">
```

Additions for other databases are welcome!


## Cache

To increase the performance of the client, all responses to HTTP requests are cached in a
sqlite database. This database is created in a 
[user's application specific cache directory](https://github.com/ActiveState/appdirs#some-example-output).
On Linux this would be `~/.cache/clldclient/db.sqlite`. The cache can be emptied by simply
removing this file, or by purging only parts of it as follows:
 
```python
>>> from clldclient.cache import Cache
>>> cache = Cache()
>>> for db in cache.stats():
...     print('{1} resources from {0} from {2} until {3}'.format(*db))
... 
6 resources from apics-online.info from 2015-07-24 11:10:23.133598 until 2015-07-24 11:52:33.972220
43 resources from wals.info from 2015-08-04 08:16:23.566448 until 2015-08-04 12:25:52.431683
11 resources from wold.clld.org from 2015-08-04 10:23:20.161135 until 2015-08-04 12:29:36.281305
>>> cache.purge(host='apics-online.info')
INFO:clldclient.cache:6 rows deleted
6
```
