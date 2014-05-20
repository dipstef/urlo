import urllib
import urllib2
from urlparse import urlparse, parse_qs, urljoin
from funlib.lazy import lazy_property, lazy
from unicoder import force_unicode, byte_string
from urlo.domain import get_domain, get_domain_suffix, parse_domain
from urlo.query import Query


class StringOrUnicode(object):

    def __new__(cls, value, *more):
        assert isinstance(value, basestring)

        bases = cls.__bases__
        if not issubclass(cls, basestring):
            bases = (value.__class__, cls) + bases
        else:
            bases = (value.__class__, ) + bases[1:]

        cls = type(cls.__name__, bases, dict(cls.__dict__))

        return value.__class__.__new__(cls, value, *more)


class Url(StringOrUnicode):

    @lazy_property
    def _parsed(self):
        return urlparse(self.unquoted(), allow_fragments=False)

    @lazy_property
    def _host_parsed(self):
        return parse_domain(self)

    @property
    def host(self):
        return self._host_parsed.domain

    @property
    def host_suffix(self):
        return self._host_parsed.suffix

    @property
    def sub_host(self):
        return self._host_parsed.sub_domain

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

    def quoted(self):
        quoted = quote(self)
        return self.__class__(quoted)

    @lazy
    def unquoted(self):
        return self.__class__(unquoted(self))

    def __new__(cls, url, *more):
        return super(Url, cls).__new__(cls, url.strip(), *more)


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