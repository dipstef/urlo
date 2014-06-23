from collections import namedtuple
import re
import urllib
import urllib2
from urlparse import parse_qs, urlparse, urljoin

from unicoder import force_unicode, byte_string

from funlib.cached import cached_property
from .domain import parse_domain
from .query import QueryParams


class UrlParsed(namedtuple('UrlParsed', ['protocol', 'host', 'port', 'path', 'query_string'])):

    def __new__(cls, protocol, host, port, path, query_string=''):
        return super(UrlParsed, cls).__new__(cls, protocol, host, int(port), path, query_string)

    @cached_property
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
        return QueryParams(parse_qs(self.query_string, keep_blank_values=True))

    def is_valid(self):
        return bool(self.protocol and self.host)

    @cached_property
    def server(self):
        return '{host}{port}'.format(host=self.host, port=':%d' % self.port if self.port != 80 else '')


class UrlParse(UrlParsed):

    def __new__(cls, url):
        parsed = urlparse(url, allow_fragments=False)

        port = parsed.port
        if port:
            host = re.sub(':%s' % str(port), '', parsed.netloc)
        else:
            host = parsed.netloc
            port = 80

        return super(UrlParsed, cls).__new__(cls, parsed.scheme, host, port, parsed.path, parsed.query)


def unquote(url):
    url_unquoted = _unquote(byte_string(url))
    return force_unicode(url_unquoted) if isinstance(url, unicode) else url_unquoted


def _unquote(url):
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


def quote(url):
    quoted = urllib.quote(byte_string(url),  _safe_chars)
    return force_unicode(quoted) if isinstance(url, unicode) else quoted


def join_url(url, path):
    return urljoin(url, unquote(path))


def is_base_url(url):
    url = UrlParse(url)
    return (not url.path or url.path == '/') and not bool(url.query_string)


def get_parameter_value(url, parameter):
    url = UrlParse(url)

    return url.query[parameter]