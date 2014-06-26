import re
import socket


class UrlError(ValueError):
    def __init__(self, url, *args, **kwargs):
        super(UrlError, self).__init__(*args, **kwargs)
        self.url = url


class InvalidScheme(UrlError):
    def __init__(self, url, scheme):
        super(InvalidScheme, self).__init__(url, scheme)


class InvalidAuthority(UrlError):
    pass


class InvalidHost(InvalidAuthority):
    def __init__(self, url, host):
        super(InvalidHost, self).__init__(url, host)


class InvalidPath(UrlError):
    def __init__(self, url, path):
        super(InvalidPath, self).__init__(url, path)


_valid_scheme = re.compile(r'^[a-z][a-z0-9+\-.]*$').match


def validate(url):
    if not url.is_relative():
        if url.scheme and not _valid_scheme(url.scheme):
            raise InvalidScheme(url, url.scheme)

        if not url.domain:
            if not is_valid_host(url.host):
                raise InvalidHost(url, url.host)
    elif not (url.scheme and url.host) and (url.path.startswith(':') or url.path.startswith('//')):
        raise InvalidPath(url, url.path)


def is_valid_host(host):
    return is_valid_ipv4(host) or is_valid_ipv6(host)


def is_valid_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        return _is_valid_inet_apton(address)
    except socket.error:  # not a valid address
        return False
    return True


def _is_valid_inet_apton(address):
    try:
        socket.inet_aton(address)
    except socket.error:
        return False
    return address.count('.') == 3


def is_valid_ipv6(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True