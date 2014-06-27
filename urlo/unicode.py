from unicoder import force_unicode
from . import UnquotedUrl
from .query import UrlQuery
from .parser import Quoted
from .url import quote, unquote, urljoin


class Url(unicode, Quoted):

    def __new__(cls, value, encoding='utf-8'):
        return super(Url, cls).__new__(cls, force_unicode(quote(value.strip()), encoding))

    def unquoted(self):
        return InternationalizedUrl(unquote(self))


class InternationalizedUrl(unicode, UnquotedUrl):

    def __new__(cls, value, encoding='utf-8'):
        return super(InternationalizedUrl, cls).__new__(cls, force_unicode(value.strip(), encoding))

    def quoted(self):
        return Url(quote(self))


def unquoted(url):
    return force_unicode(unquote(url))


def join_url(url, path):
    return urljoin(url, unquoted(path))