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

Currently, access to Glottolog data about languoids is implemented:

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


## Cache

To increase the performance of the client, all responses to HTTP requests are cached in a
sqlite database. This database is created in a 
[user's application specific cache directory](https://github.com/ActiveState/appdirs#some-example-output).
On Linux this would be `~/.cache/clldclient/db.sqlite`. The cache can be emptied by simply
removing this file, but we plan on providing functionality to invalidate parts of the
cache in a more targeted way, e.g. purging all data retrieved from Glottolog when a new 
version of Glottolog is published.