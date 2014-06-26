# coding=utf-8
from urlparse import urljoin

from urlo import Url, InternationalizedUrl
from urlo.query import parse_query, QueryParams
from urlo.unquoted import InternationalizedUrlModifier
from urlo.url import build_url, UrlBuilder, UrlModifier


url = Url('http://www.google.com/query?s=foo&bar=1')
#assert isinstance(url, str)

print url.parsed
print url.query
assert url.query == {'s': 'foo', 'bar': '1'}
assert url.domain == 'google.com'
print url.quoted()

print url.parsed
assert url.parsed == ('http', 'www.google.com', 80, '/query', 's=foo&bar=1')

assert url.domain == 'google.com'
assert url.sub_domain_name == 'www'
assert url.domain_suffix == 'com'

#url.host = 'foofle.com'
#print url.parsed
#print url

#url.query['foo'] = 2

url = Url('http://www.göögle.com/query?s=foo bar')
print url
print 'URL:', url.parsed
print type(url.query)
assert url.query['s'] == 'foo%20bar'


url = InternationalizedUrl('http://www.göögle.com/sök?s=foo bar')
print url
print 'IRI: ', url.parsed

assert url.query == {'s': 'foo bar'}
assert url.query['s'] == 'foo bar'

assert url.host == url.parsed.host == 'www.göögle.com'
assert url.path == url.parsed.path == '/sök'


url = Url('http://www.google.com/query?s=foo bar&bar=1')
print url.parsed
print url.query


url = InternationalizedUrl('http://www.google.com/query?s=foo bar&bar=1')
print url.parsed
print url.query


test = urljoin('http://test.com', u'?asd')
print test

print Url('http://www.google.com/query?s=foo&bar=1').validate()
print Url('http://long.sub.domain.at.bbc.co.uk').validate()
print Url('http://127.0.0.1/home').validate()
print Url('/home').validate()
assert Url('/home').is_relative()


print build_url(scheme='foo', host='bar.com', path='test')
builder = UrlBuilder(scheme='foo', host='bar.com', path='test')

builder.query['s'] = 1
builder.add_parameters(f=2, g=3)

print builder.url


url = UrlModifier('http://www.google.com/query?s=foo')
url.host = 'göögle.com'
print url
url.path = 'sök'
print url
url.add_parameters(t='ö')
print url
url.query['n'] = 2

print url.parsed


url = InternationalizedUrlModifier('http://www.google.com/query?s=foo')

url.host = 'göögle.com'
url.path = 'sök'
del url.query['s']
url.query['s'] = 'ö'
print url
print url.parsed

query = QueryParams.parse('s=foo')
assert query['s'] == 'foo'
query.add('s', 'bar')
assert query.get_values('s') == ['foo', 'bar']