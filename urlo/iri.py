from . import InternationalizedUrl
from .parser import UriBuilder, UriModifier


class IriBuilder(UriBuilder):
    def __init__(self, host, path='/', port=80, params=None, protocol='http'):
        super(IriBuilder, self).__init__(InternationalizedUrl, host, path, port, params, protocol)

    @property
    def iri(self):
        return self.build()


class IriModifier(UriModifier):
    def __init__(self, value):
        super(IriModifier, self).__init__(InternationalizedUrl(value))


def exclude_parameters(url, *excluded):
    iri_modifier = IriModifier(url)
    iri_modifier.remove_parameters(*excluded)

    return iri_modifier.iri


def build_iri(host, path='', port=80, params=None, protocol='http'):
    iri_build = IriBuilder(host, path, port, params, protocol)

    return iri_build.iri