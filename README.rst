Urlo
====

Url objects that extends strings objects with url parsing, manipulation and construction.

Urls
====

Extends byte string or unicode objects

.. code-block:: python

    >>> url = Url('http://www.google.com/query?s=foo&bar=1')
    assert isinstance(url, str)

    >>> url.parsed
    UrlParsed(scheme='http', host='www.google.com', port=80, path='/query', query_string='s=foo&bar=1')

    assert url.parsed == ('http', 'www.google.com', 80, '/query', 's=foo&bar=1')

    assert url.query == {'s': 'foo', 'bar': '1'}

    assert url.domain == 'google.com'
    assert url.sub_domain_name == 'www'
    assert url.domain_suffix == 'com'

Immutable by default, however exists mutable classes

.. code-block:: python

    >>> url.host = 'foofle.com'
    AttributeError("can't set attribute")

    >>> url.query['foo'] = 2
    TypeError('UrlQuery' object does not support item assignment")

Domains
=======

Uses tldextract for correct top level domain parsing:

.. code-block:: python

    >>> url = Url('http://long.sub.domain.at.bbc.co.uk')

    assert url.domain == 'bbc.co.uk'
    assert url.sub_domain_name == 'long.sub.domain.at'

Quoting
=======

Ascii characters are enforced

.. code-block:: python

    >>> url = Url('http://www.göögle.com/query?s=foo bar')
    'http://www.g%C3%B6%C3%B6gle.com/query?s=foo%20bar'

    >>> url.parsed
    UrlParsed(scheme='http', host='www.g%C3%B6%C3%B6gle.com', port=80, path='/query', query_string='s=foo%20bar')

    assert url.query['s'] == 'foo%20bar'


IRI
===

Internationalized resource identifier

.. code-block:: python

    from urlo import InternationalizedUrl

    >>> url = InternationalizedUrl('http://www.göögle.com/sök?s=foo bar')
    'http://www.göögle.com/sök?s=foo bar'

    >>> url.parsed
    UrlParsed(scheme='http', host='www.g\xc3\xb6\xc3\xb6gle.com', port=80, path='/s\xc3\xb6k', query_string='s=foo bar')

    assert url.host == url.parsed.host == 'www.göögle.com'
    assert url.path == url.parsed.path == '/sök'

    assert url.query == {'s': 'foo bar'}
    assert url.query['s'] == 'foo bar'

Validation
==========

.. code-block:: python

    >>> Url('http://www.google.com/query?s=foo&bar=1').validate()
    UrlParsed(scheme='http', host='www.google.com', port=80, path='/query', query_string='s=foo&bar=1')

    >>> Url('http://long.sub.domain.at.bbc.co.uk').validate()
    UrlParsed(scheme='http', host='long.sub.domain.at.bbc.co.uk', port=80, path='', query_string='')

    >>> Url('http://www.google/query?s=foo&bar=1').validate()
    InvalidHost('www.google')

    >>> Url('http://127.0.0.1/home').validate()
    UrlParsed(scheme='http', host='127.0.0.1', port=80, path='/home', query_string='')

    >>> Url('http://127.0.0./home').validate()
    InvalidHost('127.0.0')

    >>> Url('/home').validate()
    UrlParsed(scheme='', host='', port=80, path='/home', query_string='')
    >>> assert Url('/home').is_relative()

Building
========

.. code-block:: python

    from urlo import build_url, UrlBuilder

    >>> build_url(scheme='foo', host='bar.com', path='test')
    'foo://bar.com/test'
    >>> UrlBuilder(scheme='foo', host='bar.com', path='test')

    builder = UrlBuilder(scheme='foo', host='bar.com', path='test')

    >>> builder.query['s'] = 1
    >>> builder.add_parameters(f=2, g=3)
    >>> builder.url
    'foo://bar.com/test?s=1&g=3&f=2'


Modifying
=========

Mutable urls:

.. code-block:: python

    from urlo import UrlModifier

    >>> url = UrlModifier('http://www.google.com/query?s=foo')
    url.host = 'göögle.com'
    'http://g%C3%B6%C3%B6gle.com/query?s=foo'
    >>> url.path = 'sök'
    'http://g%C3%B6%C3%B6gle.com/s%C3%B6k?s=foo'
    >>> url.add_parameters(t=1)
    'http://g%C3%B6%C3%B6gle.com/s%C3%B6k?s=foo&t=%25C3%25B6'
    url.query['n'] = 2
    'http://g%C3%B6%C3%B6gle.com/s%C3%B6k?s=foo&t=%25C3%25B6&n=2'

    >>> url.parsed
    UrlParsed(scheme='http', host='g%C3%B6%C3%B6gle.com', port=80, path='/s%C3%B6k', query_string='s=foo&t=1&n=2')

    from urlo.unquoted import InternationalizedUrlModifier

As well internationalized urls

.. code-block:: python

    from urlo.unquoted import InternationalizedUrlModifier

    >>> url = InternationalizedUrlModifier'http://www.google.com/query?s=foo')

    >>> url.host = 'göögle.com'
    >>> url.path = 'sök'
    >>> del url.query['s']
    >>> url.query['s'] = 'ö'
    'http://göögle.com/sök?s=ö'

    >>> url.parsed
    UrlParsed(scheme='http', host='g\xc3\xb6\xc3\xb6gle.com', port=80, path='/s\xc3\xb6k', query_string='s=\xc3\xb6')

Query
=====
Supports multiple values for parameters

.. code-block:: python

    from url.query import QueryParams

    query = QueryParams.parse('s=foo')
    query.add('s', 'bar')
    assert query['s'] == 'foo'

    assert query.get_values('s') == ['foo', 'bar']