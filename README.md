Simple Solr
===========

Use Solr's API from Python with the tedious parts taken care of.

The options out there seem to require learning a whole new Api and object hirearchy. But building query URLs by hand and keeping track of `start` and `rows` was tedious and error prone. This library provides fluent interface (JQuery style) that mimics Solr parameter names. It also takes car of pulling data behind the scenes.

Supports python 2 and 3 (most likely 2.6+)

Installation
------------

Some day SimpleSolr will be a `pip install` away. But for know:

```
$ wget https://raw2.github.com/dvbalen/simple-solr/master/SimpleSolr.py  
```

And place `SimpleSolr.py` somewhere in your python library path

Usage
-----

Create a solr object an iterate over a query:
```python
 >>> import SimpleSolr
 >>>
 >>> local_core0 = SimpleSolr.select('http://localhost:8983','core0')
 >>> for row in local_core0.q(*:*):
 ...   print(row) 
 ... 
{'_version_': 1456990903946182656,
 'address_s': '920 Disc Drive Scotts Valley, CA 95066',
 'compName_s': 'Maxtor Corporation',
 'id': 'maxtor'}
{'_version_': 1456990903946182657,
 'address_s': '105 Challenger Rd. Ridgefield Park, NJ 07660-0511',
 'compName_s': 'Samsung Electronics Co. Ltd.',
 'id': 'samsung'}
{'_version_': 1456990903947231232,
 'address_s': '381 Brea Canyon Road Walnut, CA 91789-0708',
 'compName_s': 'ViewSonic Corp',
 'id': 'viewsonic'}
 >>>
```

Get the Solr query:
```python
 >>> str(local_core0.q('*:*').start(9))
 'http://localhost:8983/solr/core0/select?q=%2A%3A%2A&start=9&wt=json'
 >>> 
```

Solr queries are just iterators:
```python
 >>> ids_q = local_core.q('*:*').fl('id')
 >>> ids = [ r['id'] for id in ids_q ]
 >>> import pprint
 >>> pprint.pprint(ids)
 ['adata',
 'apple',
 'asus',
 'ati',
 'belkin',
 'canon',
 'corsair',
 'dell',
 'maxtor',
 'samsung',
 'viewsonic']
 >>>
```


Help!
----

Leave an issue or contact me @dvbalen (twitter)

TODO(?)
----

 * Package
 * Test suite
 * Facet query support
 * Less common parameters (dismax,edismax,etc)
 * Join
 * examples
