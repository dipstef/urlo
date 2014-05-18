import os

from tldextract import tldextract


_host_extract = tldextract.TLDExtract(cache_file=os.path.join(os.path.dirname(__file__), 'hosts.txt'))


def get_domain(url):
    ext = _host_extract(url.strip())
    if ext.domain and ext.suffix:
        domain = '.'.join(ext[1:])
        return domain.lower()


def get_domain_suffix(url):
    ext = _host_extract(url)
    if ext.suffix:
        return ext.suffix


def is_sub_host(url):
    ext = _host_extract(url.strip())
    return bool(ext and ext.subdomain and not ext.subdomain.startswith('www'))