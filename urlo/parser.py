from collections import namedtuple
from functools import wraps
import os
import re
from urlparse import urlparse, urlunparse

from funlib.cached import cached_property

from .domain import parse_domain
from .query import Query, UrlQuery
from .url import quote, join_url
from .query import QueryParams, UrlQueryParams
from .validation import validate, UrlError


class UrlParsed(namedtuple('UrlParsed', ['scheme', 'host', 'port', 'path', 'query_string', 'fragment'])):
    @cached_property
    def _host_parsed(self):
        return parse_domain(self.host)

    @property
    def domain(self):
        return self._host_parsed.domain

    @property
    def domain_suffix(self):
        return self._host_parsed.suffix

    @property
    def sub_domain(self):
        return self._host_parsed.sub_domain

    @property
    def sub_domain_name(self):
        return self._host_parsed.sub_domain_name

    @cached_property
    def query(self):
        return self._query_parser(self.query_string)

    @staticmethod
    def _query_parser(query_string):
        return Query.parse(query_string)

    def is_relative(self):
        return not self.host

    def is_valid(self):
        try:
            return bool(self.validate())
        except UrlError:
            return False

    def validate(self):
        validate(self)
        return self

    @cached_property
    def server(self):
        return self._type('{host}{port}').format(host=self.host, port=':%d' % self.port if self.port != 80 else '')

    @property
    def _type(self):
        unicode_url = any(isinstance(value, unicode) for value in [self.host, self.path, self.query_string])
        return unicode if unicode_url else str

    def __new__(cls, scheme, host, port, path, query_string='', fragment=''):
        return super(UrlParsed, cls).__new__(cls, scheme, host, port, path, query_string, fragment)


class UrlFragment(namedtuple('UrlParsed', ['scheme', 'host', 'port', 'path', 'query_string', 'fragment']), UrlParsed):
    pass


class UrlParse(object):
    def __new__(cls, url, with_fragments=True):
        parsed = urlparse(url, allow_fragments=with_fragments)

        port = parsed.port
        if port:
            host = re.sub(':%s' % str(port), '', parsed.netloc)
        else:
            host = parsed.netloc
            port = 80

        return cls._new(parsed.scheme, host, port, parsed.path, parsed.query, parsed.fragment)

    @classmethod
    def _new(cls, scheme, host, port, path, query_string, fragment):
        return UrlParsed(scheme, host, port, path, query_string, fragment)


class QuotedParse(UrlParse):
    @classmethod
    def _new(cls, scheme, host, port, path, query_string, fragment):
        parsed = super(QuotedParse, cls)._new(scheme, host, port, path, query_string, fragment)
        parsed._query_parser = UrlQuery.parse
        return parsed


class UrlMixin(object):
    _with_fragments = True

    @cached_property
    def parsed(self):
        return UrlParse(self, self._with_fragments)

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
        return QuotedParse(self, with_fragments=self._with_fragments)


class UriBuilder(object):
    def __init__(self, uri_class, host, path='/', port=80, params=None, scheme='http', fragment=''):
        super(UriBuilder, self).__init__()
        self.host = host
        self.path = path
        self.port = port
        self.scheme = scheme
        self.fragment = fragment
        self._uri_class = uri_class
        self.query = self._get_query_class()(params or {}, param_type=uri_class)

    def _get_query_class(self):
        return UrlQueryParams if issubclass(self._uri_class, Quoted) else QueryParams

    def _build(self):
        query_string = self._get_query_string()
        parsed = UrlParsed(self.scheme, self.host, self.port, self.path, query_string, self.fragment)

        url = self._url_type('{scheme}://{server}')
        url = url.format(scheme=parsed.scheme, server=parsed.server)
        url = join_url(url, parsed.path)
        url += parsed.query_string and '?' + parsed.query_string
        if self.fragment:
            url += '#%s' % self.fragment

        return self._uri_class(url)

    @property
    def _url_type(self):
        url_class = unicode if isinstance(self.host, unicode) or isinstance(self.path, unicode) else str
        return url_class

    def _get_query_string(self):
        query_string = self._url_type(self.query)

        if issubclass(self._uri_class, Quoted):
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


class UriModifier(UriBuilder):
    def __init__(self, uri):
        self._uri = uri
        super(UriModifier, self).__init__(uri.__class__, uri.host, uri.path, uri.port, uri.query, uri.scheme,
                                          uri.fragment)

    def __getattribute__(self, item):
        builder_fun = super(UriModifier, self).__getattribute__(item)

        if callable(builder_fun) and not item.startswith('_'):
            return self._modifier(builder_fun)

        return builder_fun

    def _modifier(self, modifier_fun):
        @wraps(modifier_fun)
        def modify(*args, **kwargs):
            modifier_fun(*args, **kwargs)

            self._update_uri()
            return self

        return modify

    def _get_query_class(self):
        query_class = super(UriModifier, self)._get_query_class()
        uri_class = self._uri_class

        class QueryModifier(query_class):
            def __init__(self, params, param_type=None):
                super(QueryModifier, self).__init__(params, param_type=param_type or uri_class)

            update = self._modifier(query_class.update)
            add = self._modifier(query_class.add)
            __setitem__ = self._modifier(query_class.__setitem__)
            __delitem__ = self._modifier(query_class.__delitem__)

        return QueryModifier

    def _update_uri(self):
        uri = super(UriModifier, self)._build()
        self._uri = uri
        self._uri_class = uri.__class__

    def __setattr__(self, name, value):
        existing_value = self.__dict__.get(name)
        super(UriModifier, self).__setattr__(name, value)

        if not name.startswith('_') and existing_value and existing_value != value:
            self._update_uri()

    def __getattr__(self, item):
        return getattr(self._uri, item)

    @property
    def __class__(self):
        return self._uri.__class__

    def __eq__(self, other):
        return self._uri == other

    def __str__(self):
        return str(self._uri)


def is_base_url(url):
    url = UrlParse(url)
    return (not url.path or url.path == '/') and not bool(url.query_string)


def get_parameter_value(url, parameter):
    url = UrlParse(url)

    return url.query[parameter]


def remove_query(url):
    parsed = urlparse(url)

    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', parsed.fragment))
