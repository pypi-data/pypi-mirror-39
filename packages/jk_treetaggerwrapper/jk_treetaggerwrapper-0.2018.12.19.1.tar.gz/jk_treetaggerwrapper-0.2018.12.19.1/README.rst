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

result = pool.tagText2("en", "The sun is shining and the children are smiling.")
```

In order to tag a text you first need to instantiate a pool of taggers. Then you can invoke `tagText2()` in order to temporarily allocate an instance of `TreeTagger` in the background and perform the PoS tagging.

NOTE: Invoking `tagText()` is discouraged as it has been replaced with a better implementation. Nevertheless it is still available for compatibility reasons.

Four arguments can be specified:

* langID : A string that contains the ID of the language of the text to tag.
* text : The text to tag.
* bWithConfidence : A boolean value that indicates whether to return the result together with confidence value or without.
* bWithNullsInsteadOfUnknown : A boolean value that indicates whether or not to convert "&gt;unknown&lt;" to a null-value.

The result is always a list with tuples. Each tuple has the following struture:

* The token itself.
* The assigned tag.
* The lemma.
* The confidence value.

The group consisting of tag-lemma-confidence can be returned multiple times. For example:

* The token itself.
* The assigned tag 1.
* The lemma 1.
* The confidence value 1.
* The assigned tag 2 (as an alternative).
* The lemma 2 (as an alternative).
* The confidence value 2 (as an alternative).

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



