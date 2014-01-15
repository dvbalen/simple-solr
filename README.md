Simple Solr
===========

A python client for Solr queries that tries to automate the tedious parts while providing a familiar interface.  

Looking at the options out there seems to require learning a whole new Api. But building query URLs by hand and keeping track of `start` and `rows` was tedious and error prone. This library provides fluent interface (JQuery style) that mimics Solr parameter names. It also takes car of pulling data behind the scenes.


Installation
------------

Some day SimpleSolr will be a `pip install` away. But for know:

```
$ wget https://raw2.github.com/dvbalen/simple-solr/master/SimpleSolr.py  
```

And place `SimpleSolr.py` somewhere in your python library path

Usage
-----

```python
 >>> import SimpleSolr
 >>>
 >>> local_core0 = SimpleSolr.select('http://localhost:8983','core0')
 >>> for row in local_core0.q(*:*):
 ...   print(row) 
 ... 
 {'compName_s': 'Maxtor Corporation', 'id': 'maxtor', 'address_s': '920 Disc Drive Scotts Valley, CA 95066', '_version_': 1456990903946182656}
(...)
 {'compName_s': 'Samsung Electronics Co. Ltd.', 'id': 'samsung', 'address_s': '105 Challenger Rd. Ridgefield Park, NJ 07660-0511', '_version_': 1456990903946182657}
 >>> str(local_core0.q('*:*').start(9))
 'http://localhost:8983/solr/core0/select?q=%2A%3A%2A&start=9&wt=json'
 >>> 
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
 * Python2 port
 * Test suite
 * Facet query support
 * Less common parameters (dismax,edismax,etc)
 * Join
 * examples
