import urllib
from urlparse import urlsplit, urlunsplit, urljoin as basejoin

from unicoder import byte_string, force_unicode


def unquote(url):
    url_unquoted = _unquote(byte_string(url))
    return force_unicode(url_unquoted) if isinstance(url, unicode) else url_unquoted


def _unquote(url):
    unquoted_url = urllib.unquote_plus(url.strip())
    while unquoted_url != url:
        url = unquoted_url
        unquoted_url = urllib.unquote_plus(url)
    return unquoted_url

# RFC 3986 (Generic Syntax)
_reserved = ';/?:@&=+$|,#'
# RFC 3986 sec 2.3
_unreserved_marks = "-_.!~*'()"
_safe_chars = urllib.always_safe + '%' + _reserved + _unreserved_marks


def quote(url):
    quoted = urllib.quote_plus(byte_string(url),  _safe_chars)
    return force_unicode(quoted) if isinstance(url, unicode) else quoted


def join_url(url, path):
    return urljoin(url, unquote(path))


def urljoin(part1, part2, *parts):
    url = basejoin(part1, part2)
    for part in parts:
        url = basejoin(url, part)
    return url


def _urljoin(*parts):
    """Normalize url parts and join them with a slash."""
    schemes, netlocs, paths, queries, fragments = zip(*(urlsplit(part) for part in parts))
    scheme, netloc, query, fragment = _first_of_each(schemes, netlocs, queries, fragments)

    path = '/'.join(x.strip('/') for x in paths if x)
    return urlunsplit((scheme, netloc, path, query, fragment))


def _first_of_each(*sequences):
    return (next((x for x in sequence if x), '') for sequence in sequences)
