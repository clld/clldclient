# clldclient

Functionality to access the API of [clld](https://github.com/clld/clld) apps, e.g.
the databases published on the [CLLD](http://clld.org) platform.

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
>>> print(apics.citation)

Michaelis, Susanne Maria & Maurer, Philippe & Haspelmath, Martin & Huber, Magnus (eds.) 2013.
Atlas of Pidgin and Creole Language Structures Online.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at http://apics-online.info, Accessed on 2015-07-24.)

>>> langs = apics.resourcemap('language')
>>> len(langs)
104
>>> list(langs.keys())[0]
u'1301'
>>> langs.url(list(langs.keys())[0])
u'http://apics-online.info/languages/1301'
>>> from pprint import pprint
>>> pprint(apics.resource('language', '1', ext='json').content)
{u'description': None,
 u'id': u'1',
 u'jsondata': {},
 u'language_pk': None,
 u'latitude': 5.833333,
 u'lexifier': u'English',
 u'longitude': -55.6,
 u'markup_description': None,
 u'name': u'Early Sranan',
 u'pk': 1,
 u'region': u'Caribbean'}
```

### Bespoke database access

#### [Glottolog](http://glottolog.org)

```python
>>> from clldclient.glottolog import Glottolog
>>> gl = Glottolog()
>>> deu = gl.languoid('deu')
>>> deu.name
u'Standard German'
>>> deu.id
u'stan1295'
>>> ie = deu.get_family(gl)
>>> ie.name
u'Indo-European'
>>> refs = list(deu.get_refs(gl))
>>> len(refs)
100  # by default only the first 100 refs are retrieved.
>>> refs[0]['name']
u'Michels, Stefan 1992'
```

#### [WALS](http://wals.info)

```python
>>> from clldclient.wals import WALS
>>> wals = WALS()
>>> l = wals.language('deu')
>>> l
<Language "Deuri">
>>> l.genus
<Genus "Bodo-Garo">
>>> l.genus.family
<Family "Sino-Tibetan">
>>> l.genus.languages
[<Language "Bodo">, <Language "Kachari">, <Language "Deuri">, <Language "Garo">, <Language "Kokborok">, <Language "Dimasa">]
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