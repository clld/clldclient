# clldclient

Functionality to access the API of [clld](https://github.com/clld/clld) apps, e.g.
the databases published on the [CLLD](http://clld.org) platform.

[![Build Status](https://travis-ci.org/clld/clldclient.svg?branch=v1.0.1)](https://travis-ci.org/clld/clldclient)
[![codecov.io](http://codecov.io/github/clld/clldclient/coverage.svg?branch=master)](http://codecov.io/github/clld/clldclient?branch=master)

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


## Usage

### Accessing clld databases generically

You can access any clld database as follows:
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

### Bespoke database access

#### [Glottolog](http://glottolog.org)

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

#### [WALS](http://wals.info)

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
>>> cache.purge(host='apics-online.info')
INFO:clldclient.cache:6 rows deleted
6
>>> cache.stats()
[]
```
