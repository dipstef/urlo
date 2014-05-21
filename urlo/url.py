from collections import namedtuple
import re
import urllib
import urllib2
from urlparse import parse_qs, urlparse, urljoin

from funlib.lazy import lazy_property
from unicoder import force_unicode, byte_string

from .domain import parse_domain
from .query import Query


def is_base_url(url):
    url = UrlParse(url)
    return (not url.path or url.path == '/') and not bool(url.query_string)


def get_parameter_value(url, parameter):
    url = UrlParse(url)

    return url.query[parameter]


class UrlParsed(namedtuple('UrlParsed', ['protocol', 'host', 'port', 'path', 'query_string'])):

    def __new__(cls, protocol, host, port, path, query_string=''):
        return super(UrlParsed, cls).__new__(cls, protocol, host, port, path, query_string)

    @lazy_property
    def _host_parsed(self):
        return parse_domain(self.host)

    @property
    def domain(self):
        return self._host_parsed.domain

    @property
    def domain_suffix(self):
        return self._host_parsed.suffix

    @property
    def sub_domain(self):
        return self._host_parsed.sub_domain

    @property
    def query(self):
        return Query(parse_qs(self.query_string, keep_blank_values=True))

    def is_valid(self):
        return bool(self.protocol and self.host)

    @lazy_property
    def server(self):
        return '{host}{port}'.format(host=self.host, port=':%d' % self.port if self.port != 80 else '')


class UrlParse(UrlParsed):

    def __new__(cls, url):
        parsed = urlparse(unquoted(url), allow_fragments=False)

        host = re.sub(':%s' % str(parsed.port), '', parsed.netloc)

        return super(UrlParsed, cls).__new__(cls, parsed.scheme, host, parsed.port, parsed.path, parsed.query)


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


def unquoted(url, encoding='utf-8'):
    url = force_unicode(unquote(quote(url)), encoding=encoding)
    return url


def join_url(url, path):
    return urljoin(url, unquoted(path))