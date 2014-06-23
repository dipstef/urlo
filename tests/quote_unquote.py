# coding=utf-8
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote, urlunquote


# coding=utf-8
from unicoder import decoded
from urlo import unquote, quote


url = u'http://test.com/link%C3%B6pings/tr%C3%A5d/%F0%9F%8D%BA'
url_utf8 = url.encode('utf-8')

unquoted = u'http://test.com/linköpings/tråd/🍺'

assert quote(url) == url
assert quote(url_utf8) == url_utf8

url_quoted = quote(unquoted)
utf8_quoted = quote(unquoted.encode('utf-8'))

assert isinstance(url_quoted, unicode)
assert isinstance(utf8_quoted, str)

assert url_quoted == url
assert utf8_quoted == url_utf8

utf8_unquoted = unquote(url_utf8)
assert isinstance(utf8_unquoted, str)

url_unquoted = unquote(url)

assert url_unquoted == unquoted
assert decoded(utf8_unquoted) == url_unquoted

django_unquoted = urlunquote(url)
assert isinstance(django_unquoted, unicode)
django_quoted = urlquote(url_unquoted)
assert isinstance(django_quoted, unicode)


assert django_unquoted == url_unquoted == unquoted

assert iri_to_uri(u'http://test.com/linköpings/tråd/🍺') == url