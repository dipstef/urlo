from . import InternationalizedUrl
from .parser import UriBuilder, UriModifier


class InternationalizedUrlBuilder(UriBuilder):
    def __init__(self, host, path='/', port=80, params=None, protocol='http'):
        super(InternationalizedUrlBuilder, self).__init__(InternationalizedUrl, host, path, port, params, protocol)

    @property
    def iri(self):
        return self.build()


class InternationalizedUrlModifier(UriModifier):
    def __init__(self, value):
        super(InternationalizedUrlModifier, self).__init__(InternationalizedUrl(value))

    @property
    def iri(self):
        return self._uri


def exclude_parameters(url, *excluded):
    iri_modifier = InternationalizedUrlModifier(url)
    iri_modifier.remove_parameters(*excluded)

    return iri_modifier.iri


def build_url(host, path='', port=80, params=None, protocol='http'):
    iri_build = InternationalizedUrlBuilder(host, path, port, params, protocol)

    return iri_build.iri


def params_url(url, params):
    if params:
        url_modifier = InternationalizedUrlModifier(url)
        url_modifier.add_parameters(**params)
        url = url_modifier.iri
    return url