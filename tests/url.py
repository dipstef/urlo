from urlo import Url, quote
from urlo.parser import is_base_url, UrlBuilder, UrlModifier


def _url_parsing_test():
    url = Url('http://test.com:81/test')

    assert url == 'http://test.com:81/test'

    assert url.port == 81
    assert url.host == 'test.com'
    assert url.host_suffix == 'com'
    assert url.path == '/test'


def _sub_domain_test():
    assert Url('www.google.co.uk').host == 'google.co.uk'
    assert Url('www.google.co.uk').host_suffix == 'co.uk'

    assert Url('sub.domain.google.com').host == 'google.com'
    assert Url('sub.domain.google.co.uk').host == 'google.co.uk'


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
    url = 'http://test.com/test?foo=123&bar=456'
    assert 'http://test.com/test?bar=456' == UrlModifier(url).remove_parameters('foo')


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
    _sub_domain_test()
    _base_url_test()

    _url_parameters_test()

    _url_builder_test()

    _url_quoting_test()


if __name__ == '__main__':
    main()