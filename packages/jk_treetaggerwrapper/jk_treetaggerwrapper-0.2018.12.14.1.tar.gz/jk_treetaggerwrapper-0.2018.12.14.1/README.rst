jk_treetaggerwrapper
====================

Introduction
------------

This python module provides a wrapper around treetagger. Currently this module makes use of module `treetaggerwrapper` but this depency will be changed in the future.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-treetaggerwrapper)
* [pypi.python.org](https://pypi.python.org/pypi/jk_treetaggerwrapper)

How to use this module
----------------------

Example:

```python
pool = PoolOfThreadedTreeTaggers("/path/to/treetagger")

result = pool.tagText("en", "The sun is shining and the children are smiling.")
```

In order to tag a text you first need to instantiate a pool of taggers. Then you can invoke `tagText()` in order to temporarily allocate an instance of `TreeTagger` in the background and perform the PoS tagging.

Concurrency
-----------

Please note that this library is based on `treetaggerwrapper` which follows a thread-based concurrency model. On tagging `treetaggerwrapper` instantiates a TreeTagger background process that is alive for the duration of the `treetaggerwrapper` object. This `treetaggerwrapper` object then communicates with this background process and uses threads for this purpose. Therefor the class `PoolOfThreadedTreeTaggers` provided by `jk_treetaggerwrapper` is bound to this limitation.

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



