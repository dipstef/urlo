from urlo import Url, InternationalizedUrl


def _with_fragment_test():
    url = Url('http://test.com?foo=bar#1234', with_fragments=True)
    assert url.fragment == '1234'

def _without_fragment_test():
    url = Url('http://test.com?foo=bar#1234', with_fragments=False)
    assert not url.fragment
    assert url.query['foo'] == 'bar%231234'


def _iri_with_fragment_test():
    url = InternationalizedUrl('http://test.com?foo=bar#1234', with_fragments=True)
    assert url.fragment == '1234'

def _iri_without_fragment_test():
    url = InternationalizedUrl('http://test.com?foo=bar#1234', with_fragments=False)
    assert not url.fragment
    assert url.query['foo'] == 'bar#1234'



def main():
    _with_fragment_test()
    _without_fragment_test()

    _iri_with_fragment_test()
    _iri_without_fragment_test()


if __name__ == '__main__':
    main()
