import re

from urlo.url import unquoted as base_unquoted, join_url


def join_url(url, path):
    return remove_ending_slash(base_join(url, path))


def unquoted(url):
    return remove_ending_slash(base_unquoted(url))


_ending_slash = re.compile('/+$')


def remove_ending_slash(url):
    return _ending_slash.sub('', url)