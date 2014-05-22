from urlparse import urljoin, urlparse, urlunparse
from . import Url, UrlParse
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
        return self.parsed.url

    @property
    def parsed(self):
        return UrlRebuild(self.protocol, self.host, self.port, self.path, str(self.query))

    def __getitem__(self, item):
        return self.query.get(item)

    def __setitem__(self, key, value):
        self.query[key] = value

    def __delitem__(self, key):
        self.query.remove([key])

    def remove_parameters(self, *params):
        self.query.remove(*params)

    def add_parameters(self, **params):
        self.query.update(params)


class UrlRebuild(UrlParsed):

    @property
    def url(self):
        url = '{protocol}://{server}'.format(protocol=self.protocol, server=self.server)

        url = urljoin(url, self.path + self.query_string)

        return Url(url)


class UrlModifier(UrlBuilder):

    def __init__(self, url):
        url = UrlParse(url)
        super(UrlModifier, self).__init__(url.host, url.path, url.port, url.query, url.protocol)


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