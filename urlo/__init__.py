from funlib.cached import cached, cached_property

from .domain import get_domain, get_domain_suffix, parse_domain
from .url import UrlParse, quote, unquote, QuotedParse, join_url
from .query import QueryParams


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


class UrlMixin(object):

    @cached_property
    def parsed(self):
        return UrlParse(self)

    def __getattr__(self, item):
        return getattr(self.parsed, item)

    def __setattr__(self, name, value):
        if not name.startswith('_') and hasattr(self.parsed, name):
            setattr(self.parsed, name, value)
        else:
            super(UrlMixin, self).__setattr__(name, value)

    def join_to(self, other):
        return self.__class__(join_url(self, other))


class Quoted(UrlMixin):

    @cached_property
    def parsed(self):
        return QuotedParse(self)

    @cached
    def quoted(self):
        return self.__class__(quote(self))

    @cached
    def unquoted(self):
        return InternationalizedUrl(unquote(self))


class Url(StringOrUnicode, Quoted):

    def __new__(cls, value, *more):
        return super(Url, cls).__new__(cls, quote(value.strip()), *more)


class Unquoted(UrlMixin):

    @cached
    def quoted(self):
        return Url(quote(self))

    @cached
    def unquoted(self):
        return self.__class__(unquote(self))


class InternationalizedUrl(StringOrUnicode, Unquoted):

    def __new__(cls, value, *more):
        return super(InternationalizedUrl, cls).__new__(cls, value.strip(), *more)