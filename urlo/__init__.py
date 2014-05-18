import urllib
import urllib2
from urlparse import urlparse, parse_qs, urljoin
from funlib.lazy import lazy_property, lazy
from unicoder import force_unicode, byte_string
from urlo.domain import get_domain, get_domain_suffix
from urlo.query import Query


def _url(value):
    assert isinstance(value, basestring)

    class Url(type(value)):

        @lazy_property
        def _parsed(self):
            return urlparse(self.unquoted(), allow_fragments=False)

        @property
        def host(self):
            return get_domain(self)

        @property
        def host_suffix(self):
            return get_domain_suffix(self)

        @property
        def protocol(self):
            return self._parsed.scheme

        @property
        def query_string(self):
            return self._parsed.query

        @property
        def query(self):
            query = parse_qs(self._parsed.query, keep_blank_values=True)
            return Query(query)

        @property
        def path(self):
            return self._parsed.path

        @property
        def port(self):
            return self._parsed.port or 80

        def is_valid(self):
            return bool(self.protocol and self.host)

        @lazy
        def quoted(self):
            return Url(quote(self))

        @lazy
        def unquoted(self):
            return Url(unquoted(self))

    return Url(value.strip())

Url = _url


def unquoted(url, encoding='utf-8'):
    url = force_unicode(unquote(quote(url)), encoding=encoding)
    return url


def unquote(url):
    unquoted_url = urllib2.unquote(url.strip())
    while unquoted_url != url:
        url = unquoted_url
        unquoted_url = urllib2.unquote(url)

    return unquoted_url


# RFC 3986 (Generic Syntax)
_reserved = ';/?:@&=+$|,#'
# RFC 3986 sec 2.3
_unreserved_marks = "-_.!~*'()"
_safe_chars = urllib.always_safe + '%' + _reserved + _unreserved_marks


def quote(url, encoding='utf-8'):
    s = byte_string(url, encoding)
    return urllib.quote(s,  _safe_chars)


def join_url(url, path):
    return urljoin(url, unquoted(path))