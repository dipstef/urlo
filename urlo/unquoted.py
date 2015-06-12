from . import InternationalizedUrl
from .parser import UriBuilder, UriModifier


class InternationalizedUrlBuilder(UriBuilder):
    def __init__(self, host, path='/', port=80, params=None, scheme='http'):
        super(InternationalizedUrlBuilder, self).__init__(InternationalizedUrl, host, path, port, params, scheme)

    @property
    def iri(self):
        return self._build()


class InternationalizedUrlModifier(UriModifier):
    def __init__(self, value, with_fragments=True):
        super(InternationalizedUrlModifier, self).__init__(InternationalizedUrl(value, with_fragments=with_fragments))

    @property
    def iri(self):
        return self._uri


def exclude_parameters(url, *excluded):
    iri_modifier = InternationalizedUrlModifier(url, with_fragments=True)
    iri_modifier.remove_parameters(*excluded)

    return iri_modifier.iri


def build_url(host, path='', port=80, params=None, scheme='http'):
    iri_build = InternationalizedUrlBuilder(host, path, port, params, scheme)

    return iri_build.iri


def params_url(url, params):
    if params:
        url_modifier = InternationalizedUrlModifier(url)
        url_modifier.add_parameters(**params)
        url = url_modifier.iri
    return url