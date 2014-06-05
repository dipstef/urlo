from functools import wraps
import os
from urlparse import urljoin, urlparse, urlunparse

from . import Url
from .query import Query
from .url import UrlParsed


class UrlBuilder(object):

    def __init__(self, host, path='/', port=80, params=None, protocol='http'):
        super(UrlBuilder, self).__init__()
        self.host = host
        self.path = path
        self.port = port
        self.query = Query(params or {})
        self.protocol = protocol

    @property
    def url(self):
        parsed = UrlRebuild(self.protocol, self.host, self.port, self.path, unicode(self.query))
        return parsed.url

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


class UrlRebuild(UrlParsed):

    @property
    def url(self):
        url = '{protocol}://{server}'.format(protocol=self.protocol, server=self.server)

        url = urljoin(url, self.path + self.query_string)

        return Url(url)


class UrlModifier(object):

    def __init__(self, value):
        self.url = Url(value)
        self._builder = UrlBuilder(self.host, self.path, self.port, self.query, self.protocol)

    def __getattr__(self, item):
        try:
            return getattr(self.url, item)
        except AttributeError:
            builder_fun = getattr(self._builder, item)

            @wraps(builder_fun)
            def modify(*args, **kwargs):
                builder_fun(*args, **kwargs)
                self.url = self._builder.url
                return self

            return modify

    @property
    def __class__(self):
        return self.url.__class__

    def __eq__(self, other):
        return self.url == other

    def __repr__(self):
        return repr(self.url)


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