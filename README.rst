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
    UrlParsed(protocol='http', host='www.google.com', port=80, path='/query', query_string='s=foo&bar=1')

    assert url.query == {'s': 'foo', 'bar': '1'}
