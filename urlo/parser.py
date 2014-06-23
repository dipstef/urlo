from functools import wraps
import os
from urlparse import urljoin, urlparse, urlunparse

from . import Url, Quoted, quote
from .query import Query
from .url import UrlParsed


class UriBuilder(object):

    def __init__(self, uri_class, host, path='/', port=80, params=None, protocol='http'):
        super(UriBuilder, self).__init__()
        self.host = host
        self.path = path
        self.port = port
        self.query = Query(params or {})
        self.protocol = protocol
        self._uri_class = uri_class

    def build(self):
        query_string = self._get_query_string()
        parsed = UrlParsed(self.protocol, self.host, self.port, self.path, query_string)
        url = '{protocol}://{server}'.format(protocol=parsed.protocol, server=parsed.server)
        url = urljoin(url, parsed.path + parsed.query_string)

        return self._uri_class(url)

    def _get_query_string(self):
        url_class = unicode if isinstance(self.host, unicode) or isinstance(self.path, unicode) else str

        query_string = url_class(self.query)

        if isinstance(self._uri_class, Quoted):
            query_string = quote(query_string)

        return query_string

    def join_path(self, *entries):
        if entries:
            self.path = os.path.join(self.path, *entries)

    def add_parameters(self, **params):
        self.query.update(params)

    def remove_parameters(self, *params):
        self.query.remove(*params)

    def __getitem__(self, item):
        return self.query[item]

    def __setitem__(self, key, value):
        self.query[key] = value

    def __delitem__(self, key):
        self.query.remove([key])


class UrlBuilder(UriBuilder):

    def __init__(self, host, path='/', port=80, params=None, protocol='http', url_class=Url):
        super(UrlBuilder, self).__init__(url_class, host, path, port, params, protocol)

    @property
    def url(self):
        return self.build()


class UriModifier(object):

    def __init__(self, uri):
        self._uri = uri

    def __getattr__(self, item):
        try:
            return getattr(self._uri, item)
        except AttributeError:
            builder = UriBuilder(self.__class__, self.host, self.path, self.port, self.query, self.protocol)

            builder_fun = getattr(builder, item)

            @wraps(builder_fun)
            def modify(*args, **kwargs):
                builder_fun(*args, **kwargs)

                uri = builder.build()
                self._uri = uri
                return self

            return modify

    @property
    def __class__(self):
        return self._uri.__class__

    def __eq__(self, other):
        return self._uri == other

    def __repr__(self):
        return repr(self._uri)


class UrlModifier(UriModifier):
    _url_class = Url

    def __init__(self, value):
        super(UrlModifier, self).__init__(self._url_class(value))

    @property
    def url(self):
        return self._uri


def exclude_parameters(url, *excluded):
    url_modifier = UrlModifier(url)
    url_modifier.remove_parameters(*excluded)

    return url_modifier.url


def remove_query(url):
    parsed = urlparse(url)

    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))


def build_url(host, path='', port=80, params=None, protocol='http'):
    url_build = UrlBuilder(host, path, port, params, protocol)

    return url_build.url


def params_url(url, params):
    if params:
        url_modifier = UrlModifier(url)
        url_modifier.add_parameters(**params)
        url = url_modifier.url
    return url