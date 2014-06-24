# coding=utf-8
from urlparse import urljoin

from urlo import Url, InternationalizedUrl


url = Url('http://www.google.com/query?s=foo&bar=1')
#assert isinstance(url, str)

print url.parsed
print url.query
assert url.query == {'s': 'foo', 'bar': '1'}
assert url.domain == 'google.com'
print url.quoted()

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