from urlo import Url, quote
from urlo.parser import UrlBuilder, UrlModifier
from urlo.url import is_base_url


def _url_parsing_test():
    url = Url('http://test.com:81/test')

    assert url == 'http://test.com:81/test'

    assert url.port == 81
    assert url.host == 'test.com'
    assert url.domain == 'test.com'
    assert url.domain_suffix == 'com'
    assert url.path == '/test'


def _ip_url_test():
    url = Url('http://192.168.1.1:81/test')

    assert url.port == 81
    assert not url.domain
    assert not url.sub_domain
    assert not url.domain_suffix

    assert url.host == '192.168.1.1'


def _sub_domain_test():
    google_co_uk = Url('http://www.google.co.uk')

    assert google_co_uk.port == 80
    assert google_co_uk.host == 'www.google.co.uk'
    assert google_co_uk.domain == 'google.co.uk'
    assert google_co_uk.domain_suffix == 'co.uk'

    google_sub_domain = Url('http://sub.domain.google.com')

    assert google_sub_domain.domain == 'google.com'
    assert google_sub_domain.host == 'sub.domain.google.com'
    assert google_sub_domain.sub_domain == 'sub.domain.google.com'


def _base_url_test():
    assert 'http://asd.com/' == Url('http://asd.com/')
    assert is_base_url('http://asd.com/')
    assert is_base_url('http://asd.com?')
    assert not is_base_url('http://asd.com?foo=123')
    assert not is_base_url('http://asd.com/asd')
    assert not is_base_url('http://asd.com/asd?foo=123')
    assert not is_base_url('http//asd.com/test.jpg')


def _url_parameters_test():
    url = Url('http://test.com/test?foo=123&bar=56')

    assert url.query['foo'] == '123'
    assert url.query['bar'] == '56'
    assert url.query == {'foo': '123', 'bar': '56'}


def _url_builder_test():
    url_build = UrlBuilder('test.com', 'test')
    assert 'http://test.com/test' == url_build.url

    url_build.add_parameters(foo=123, bar=456)

    assert 'http://test.com/test?foo=123&bar=456' == url_build.url

    url_build.remove_parameters('foo')
    assert 'http://test.com/test?bar=456' == url_build.url
    url_build.remove_parameters()

    assert 'http://test.com/test' == url_build.url
    url_build['foo'] = 123
    url_build['foo'] = 456

    assert url_build.query == {'foo': ['123', '456']}
    assert url_build['foo'] == '123'
    assert url_build.query.get_values('foo') == ['123', '456']

    assert url_build.url == 'http://test.com/test?foo=123&foo=456'

    url = Url('http://test.com/test?foo=123 456')
    assert url.query['foo'] == '123 456'


def _url_modification_test():
    url = UrlModifier('http://test.com/test?foo=123&bar=456')
    modified = url.remove_parameters('foo')
    assert 'http://test.com/test?bar=456' == modified
    assert isinstance(modified, unicode)

    url = UrlModifier('http://192.168.1.1:81/test?foo=123')
    modified = url.add_parameters(bar=456)
    assert 'http://192.168.1.1:81/test?foo=123&bar=456' == modified

    assert modified.url == modified


def _url_quoting_test():
    url = Url('http://test.com/test?foo=123 456')
    assert 'http://test.com/test?foo=123%20456' == url.quoted()
    url = Url('http://test.com/test?foo=123 456')

    quoted = quote(quote(quote(url)))
    assert 'http://test.com/test?foo=123%20456' == quoted
    url = Url(quoted)
    assert 'http://test.com/test?foo=123 456' == url.unquoted()


def main():
    _url_parsing_test()
    _ip_url_test()
    _sub_domain_test()
    _base_url_test()

    _url_parameters_test()

    _url_builder_test()
    _url_modification_test()

    _url_quoting_test()


if __name__ == '__main__':
    main()