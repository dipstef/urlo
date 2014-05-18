from urlparse import urlparse, urlunparse, urljoin

from urlo import Url, unquoted
from urlo.query import Query


class UrlBuilder(object):

    def __init__(self, host, path='', port=80, params=None, protocol='http'):
        self.host = host
        self.path = path
        self.port = port
        self.query = Query(params or {})
        self.protocol = protocol

    @property
    def url(self):
        url = '{protocol}://{host}{port}'.format(protocol=self.protocol, host=self.host,
                                                 port=':%d' % self.port if self.port != 80 else '')

        url = urljoin(url, self.path)
        url += str(self.query)

        return Url(url)

    @property
    def _parsed(self):
        return urlparse(unquoted(self.url), allow_fragments=False)

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


class UrlModifier(object):

    def __init__(self, url):
        url = Url(url)
        self._builder = UrlBuilder(url.host, url.path, url.port, url.query, url.protocol)
        self.url = url

    def remove_parameters(self, *params):
        self._builder.remove_parameters(*params)
        self.url = Url(self._builder.url)

    def add_parameters(self, **params):
        self._builder.add_parameters(**params)
        self.url = Url(self._builder.url)


def is_base_url(url):
    url = Url(url)
    return (not url.path or url.path == '/') and not bool(url.query_string)


def exclude_parameters(url, *excluded):
    url_modifier = UrlModifier(url)
    url_modifier.remove_parameters(*excluded)

    return url_modifier.url


def remove_query(url):
    parsed = urlparse(url)

    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))


def get_parameter_value(url, parameter):
    url = Url(url)

    return url[parameter]


def build_url(host, path='', port=80, params=None, protocol='http'):
    url_build = UrlBuilder(host, path, port, params, protocol)

    return url_build.url


def params_url(url, params):
    if params:
        url_modifier = UrlModifier(url)
        url_modifier.add_parameters(**params)
        url = url_modifier.url
    return url