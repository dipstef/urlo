from funlib.cached import cached, cached_property

from .domain import get_domain, get_domain_suffix, parse_domain

from .url import UrlParse, quote, unquote

from .query import Query
from urlo.url import unquoted


class StringOrUnicode(object):

    def __new__(cls, value, *more):
        assert isinstance(value, basestring)

        bases = cls.__bases__
        if not issubclass(cls, basestring):
            bases = (value.__class__, cls) + bases
        else:
            bases = (value.__class__, ) + bases[1:]

        cls = type(cls.__name__, bases, dict(cls.__dict__))

        return value.__class__.__new__(cls, value, *more)


class Url(StringOrUnicode):

    def __init__(self, value, *args):
        super(Url, self).__init__(value, *args)

    def __new__(cls, value, *more):
        return super(Url, cls).__new__(cls, value.strip(), *more)

    @cached_property
    def parsed(self):
        return UrlParse(self)

    @cached
    def quoted(self):
        quoted = quote(self)
        return self.__class__(quoted)

    @cached
    def unquoted(self):
        return self.__class__(unquoted(self))

    def __getattr__(self, item):
        return getattr(self.parsed, item)