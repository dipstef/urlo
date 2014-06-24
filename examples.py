from urlparse import urljoin

from urlo import Url, InternationalizedUrl


url = Url('http://www.google.com/query?s=foo&bar=1')
#assert isinstance(url, str)

print url.parsed
print url.query
assert url.query == {'s': 'foo', 'bar': '1'}
assert url.domain == 'google.com'
print url.quoted()


url = Url('http://www.google.com/query?s=foo bar&bar=1')
print url.parsed
print url.query


url = InternationalizedUrl('http://www.google.com/query?s=foo bar&bar=1')
print url.parsed
print url.query


test = urljoin('http://test.com', u'?asd')
print test