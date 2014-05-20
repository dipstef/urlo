from urlo import Url


class UrlSubClass(Url):
    @property
    def foo(self):
        return 'foo'


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
    assert isinstance(quoted, str)

    url = UrlSubClass(u'http://test.com')

    assert isinstance(url, UrlSubClass)
    assert 'foo' == url.foo
    assert isinstance(url, Url)
    assert isinstance(url, unicode)

if __name__ == '__main__':
    main()