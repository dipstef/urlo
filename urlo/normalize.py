import re
from urlparse import urljoin
from .unicode import unquoted as unquoted_unicode


def join_url(url, path):
    return remove_ending_slash(urljoin(url, unquoted_unicode(path)))


def unquoted(url):
    return remove_ending_slash(unquoted_unicode(url))


_ending_slash = re.compile('/+$')


def remove_ending_slash(url):
    return _ending_slash.sub('', url)