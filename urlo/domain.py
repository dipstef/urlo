from collections import namedtuple
import os
from tldextract import tldextract
from unicoder import byte_string, decoded


_host_extract = tldextract.TLDExtract(cache_file=os.path.join(os.path.dirname(__file__), 'hosts.txt'))


def get_domain(url):
    ext = _host_extract(byte_string(url.strip()))
    return _to_original_str(url, _domain(ext))


def _domain(ext):
    if ext.domain and ext.suffix:
        domain = '.'.join(ext[1:])
        return domain.lower()


def get_domain_suffix(url):
    ext = _host_extract(url)
    if ext.suffix:
        return _to_original_str(url, ext.suffix)


def get_sub_domain(url):
    ext = _host_extract(url.strip())
    return _to_original_str(url, _sub_domain(ext))


def _sub_domain(ext):
    sub_domain = _sub_domain_name(ext)
    domain = _domain(ext)
    return '.'.join((sub_domain, domain)) if sub_domain else domain


def get_sub_domain_name(url):
    ext = _host_extract(url.strip())
    return _to_original_str(url, _sub_domain_name(ext))


def _sub_domain_name(ext):
    return ext.subdomain.lower() if ext.subdomain else None


def parse_domain(url):
    ext = _host_extract(url.strip())
    return DomainInfo(_sub_domain_name(ext), _domain(ext), ext.suffix)


def _to_original_str(url, value):
    return decoded(value) if value and isinstance(url, unicode) else value


class DomainInfo(namedtuple('DomainInfo', ['sub_domain_name', 'domain', 'suffix'])):
    def __new__(cls, sub_domain_name, domain, suffix):
        return super(DomainInfo, cls).__new__(cls, sub_domain_name, domain, suffix)

    @property
    def sub_domain(self):
        return '.'.join((self.sub_domain_name, self.domain)) if self.sub_domain_name else self.domain