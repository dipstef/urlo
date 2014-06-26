from urlo import Url, UrlModifier


class UrlSubClass(Url):
    @property
    def foo(self):
        return 'foo'

foo = UrlSubClass


def main():
    url = Url('http://test.com')

    assert isinstance(url, str)
    assert isinstance(url, Url)
    assert 'test.com' == url.host

    url = Url(u'http://test.com')

    assert isinstance(url, unicode)
    assert isinstance(url, Url)
    assert 'test.com' == url.host

    quoted = url.quoted()
    assert isinstance(quoted, Url)
    assert isinstance(quoted, unicode)

    url = UrlSubClass(u'http://test.com')

    assert isinstance(url, UrlSubClass)
    assert 'foo' == url.foo
    assert isinstance(url, Url)
    assert isinstance(url, unicode)

    url = Url('http://test.com')
    url = url.__class__('http://test.com')
    assert url.host == 'test.com'

    modifier = UrlModifier('http://test.com')

    modifier.join_path('foo')
    assert modifier.host == 'test.com'

    modifier.add_parameters(foo=1)
    assert modifier.host == 'test.com'

    modifier.remove_parameters('foo')
    assert modifier.host == 'test.com'

    url = UrlModifier('http://test.com/test')
    url.remove_parameters('foo')

    url.join_path(u'foo')

    assert url == u'http://test.com/test/foo'
    assert isinstance(url, unicode)

    url = Url(u'http://test.com?s=foo')
    assert isinstance(url.query['s'], unicode)

    url = Url('http://test.com?s=foo')
    assert isinstance(url.query['s'], str)


if __name__ == '__main__':
    main()