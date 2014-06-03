from collections import OrderedDict

from unicoder import byte_string, decoded


class Query(object):

    def __init__(self, query):
        params = ((param, _param_value(query[param])) for param in query)
        self._params = OrderedDict(params)

    def __getitem__(self, parameter):
        value = self._params[parameter]

        return _param_value(value)

    def __setitem__(self, parameter, value):
        value = str(value)
        existing = self._params.get(parameter)
        if existing:
            value = [existing, value] if not isinstance(existing, list) else existing + [value]

        self._params[parameter] = value

    def get(self, parameter):
        try:
            return self[parameter]
        except KeyError:
            return None

    def get_values(self, parameter):
        values = self._params.get(parameter, [])
        return values if isinstance(values, list) else [values]

    def iterate_query_values(self):
        return ((param, value) for param, values in self.iterate_query_value_list() for value in values)

    def iterate_query_value_list(self):
        return ((param, self.get_values(param)) for param in self._params.iterkeys())

    def remove(self, *parameters):
        parameters = parameters or self._params.iterkeys()
        for parameter in parameters:
            if parameter in self:
                del self._params[parameter]

    def __str__(self):
        values = ('%s=%s' % (param, byte_string(value or '')) for param, value in self.iterate_query_values())
        query = '&'.join(values)
        return '?' + query if query else ''

    def __unicode__(self):
        return decoded(str(self))

    def keys(self):
        return self._params.keys()

    def __iter__(self):
        return iter(self._params)

    def __repr__(self):
        return repr(self._params)

    def __eq__(self, other):
        return self._params == other

    def __len__(self):
        return len(self._params)

    def update(self, params):
        self._params.update(Query(params))

    def iteritems(self):
        return self._params.iteritems()


def _param_value(value):
    return value[0] if isinstance(value, list) else value