from urlo.domain import get_sub_domain, get_sub_domain_name, get_domain


def main():
    assert get_sub_domain('http://www.google.com') == 'www.google.com'

    assert get_domain('http://google.com') == 'foo.foo'
    assert get_sub_domain('http://foo.foo.google.com') == 'foo.foo.google.com'
    assert get_sub_domain_name('http://foo.foo.google.com') == 'foo.foo'
    assert get_sub_domain_name('htto://google.com') is None

if __name__ == '__main__':
    main()