from collections import OrderedDict
import urllib
from urlparse import parse_qs
from unicoder import byte_string, decoded, force_unicode


class Query(object):

    def __init__(self, query=None, param_type=str):
        query = query or {}
        self._param_type = byte_string if param_type is str else force_unicode
        params = ((param, self._param_value(query[param])) for param in query)
        self._params = OrderedDict(params)

    @classmethod
    def parse(cls, query_string):
        query_data = parse_qs(query_string, keep_blank_values=True)
        return cls(query_data, param_type=type(query_string))

    def __getitem__(self, parameter):
        value = self._params[parameter]

        return value[0] if isinstance(value, list) else value

    def get(self, parameter, default=None):
        try:
            return self[parameter]
        except KeyError:
            return default

    def get_values(self, parameter):
        values = self._params.get(parameter, [])
        return values if isinstance(values, list) else [values]

    def iterate_query_values(self):
        return ((param, value) for param, values in self.iterate_query_value_list() for value in values)

    def iterate_query_value_list(self):
        return ((param, self.get_values(param)) for param in self._params.iterkeys())

    def __str__(self):
        values = ((byte_string(param), byte_string(value)) for param, value in self.iterate_query_values())
        values = ('%s%s' % (param, '=' + value if value else '') for param, value in values)
        query = '&'.join(values)
        return query

    def __unicode__(self):
        return decoded(str(self))

    def keys(self):
        return self._params.keys()

    def iteritems(self):
        return self._params.iteritems()

    def __iter__(self):
        return iter(self._params)

    def __repr__(self):
        return repr(self._params)

    def __eq__(self, other):
        return self._params == other

    def __len__(self):
        return len(self._params)

    def _param_value(self, value):
        if isinstance(value, list):
            if len(value) > 1:
                return map(self._param_type, value)
            else:
                value = value[0]
        return self._param_type(value)


class QueryUpdate(object):

    def add(self, parameter, value):
        value = str(value)
        existing = self._params.get(parameter)
        if existing:
            value = [existing, value] if not isinstance(existing, list) else existing + [value]
        self._params[parameter] = value

    def __setitem__(self, parameter, value):
        self._params[parameter] = value

    def __delitem__(self, parameter):
        del self._params[parameter]

    def remove(self, *parameters):
        parameters = parameters or self._params.iterkeys()
        for parameter in parameters:
            if parameter in self:
                del self._params[parameter]

    def update(self, params):
        self._params.update(self.__class__(params))


class UrlQuery(Query):

    def __init__(self, query=None, param_type=str):
        self._param_type = byte_string if param_type is str else force_unicode
        super(UrlQuery, self).__init__(self._quote_params(query), param_type)

    def _quote_params(self, params):
        params = dict(params)

        for key, value in params.iteritems():
            value = self._quote_param(value)
            params[key] = value
        return params

    def _quote_param(self, value):
        value = self._param_value(value)
        if isinstance(value, list):
            value = map(self._quote, value)
        else:
            value = self._quote(value)
        return value

    def _quote(self, value):
        return urllib.quote_plus(value)


class UrlQueryParams(UrlQuery, QueryUpdate):

    def __init__(self, query=None, param_type=str):
        super(UrlQueryParams, self).__init__(query, param_type)

    def __setitem__(self, parameter, value):
        super(UrlQueryParams, self).__setitem__(parameter, self._quote_param(value))

    def update(self, params):
        super(UrlQueryParams, self).update(self._quote_params(params))


class QueryParams(UrlQueryParams):
    _reserved = frozenset((c for c in ';/?:@&=+$|,#'))

    def _quote(self, value):
        result = ''.join(map(lambda c: urllib.quote(c) if c in self._reserved else c, value))
        return result


def parse_query(query_string):
    return QueryParams.parse(query_string)


def quoted_query(query_string):
    return UrlQueryParams.parse(query_string)