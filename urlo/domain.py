import os

from tldextract import tldextract


_host_extract = tldextract.TLDExtract(cache_file=os.path.join(os.path.dirname(__file__), 'hosts.txt'))


def get_domain(url):
    ext = _host_extract(url.strip())
    return _domain(ext)


def _domain(ext):
    if ext.domain and ext.suffix:
        domain = '.'.join(ext[1:])
        return domain.lower()


def get_domain_suffix(url):
    ext = _host_extract(url)
    if ext.suffix:
        return ext.suffix


def get_subdomain(url):
    ext = _host_extract(url.strip())
    subdomain = ext.subdomain.lower() if ext.subdomain else ''

    domain = _domain(ext)

    return '.'.join((subdomain, domain)) if subdomain else domain


def get_subdomain_name(url):
    ext = _host_extract(url.strip())
    return ext.subdomain.lower() if ext.subdomain else None