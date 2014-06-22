Urlo
====

Url objects that extends strings objects with url parsing, manipulation and construction.

Urls
====

Extend byte string or unicode classes:

.. code-block:: python

    >>> url = Url('http://www.google.com/query?s=foo&bar=1')
    assert isinstance(url, str)

    >>> url.parsed
    UrlParsed(protocol=u'http', host=u'www.google.com', port=80, path=u'/query', query_string=u's=foo&bar=1')