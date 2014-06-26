from funlib.cached import cached

from .domain import get_domain, get_domain_suffix, parse_domain
from .parser import UrlParse, QuotedParse
from .query import QueryParams
from .url import quote, unquote, join_url
from .parser import UriBuilder, UriModifier, UrlMixin, Quoted


class StringOrUnicode(object):

    def __new__(cls, value, *more):
        assert isinstance(value, basestring)

        text_class = cls._get_text_class()

        bases = [base_class for base_class in cls.__bases__ if base_class != StringOrUnicode]
        if not text_class:
            bases = (cls, value.__class__, ) + tuple(bases)
            cls = type(cls.__name__, bases, dict(cls.__dict__))
        elif text_class != value.__class__:
            bases = bases[1:]
            bases[bases.index(text_class)] = value.__class__
            bases = tuple([cls._original_class()] + bases)
            cls = type(cls.__name__, bases, dict(cls.__dict__))

        return value.__class__.__new__(cls, value, *more)

    @classmethod
    def _get_text_class(cls):
        for base_class in cls.__bases__:
            if base_class == str or base_class == unicode:
                return base_class

    @classmethod
    def _original_class(cls):
        bases = cls.__bases__
        return cls if StringOrUnicode in bases else bases[0]._original_class()


class QuotedUrl(Quoted):

    @cached
    def quoted(self):
        return self.__class__(quote(self))

    @cached
    def unquoted(self):
        return InternationalizedUrl(unquote(self))


class Url(StringOrUnicode, QuotedUrl):

    def __new__(cls, value, *more):
        return super(Url, cls).__new__(cls, quote(value.strip()), *more)


class UnquotedUrl(UrlMixin):

    @cached
    def quoted(self):
        return Url(quote(self))

    @cached
    def unquoted(self):
        return self.__class__(unquote(self))


class InternationalizedUrl(StringOrUnicode, UnquotedUrl):

    def __new__(cls, value, *more):
        return super(InternationalizedUrl, cls).__new__(cls, value.strip(), *more)


class UrlBuilder(UriBuilder):

    def __init__(self, host, path='/', port=80, params=None, scheme='http', url_class=Url):
        super(UrlBuilder, self).__init__(url_class, host, path, port, params, scheme)

    @property
    def url(self):
        return self._build()


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


def build_url(host, path='', port=80, params=None, scheme='http'):
    url_build = UrlBuilder(host, path, port, params, scheme)

    return url_build.url


def params_url(url, params):
    if params:
        url_modifier = UrlModifier(url)
        url_modifier.add_parameters(**params)
        url = url_modifier.url
    return url