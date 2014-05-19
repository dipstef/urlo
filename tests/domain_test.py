from urlo.domain import get_subdomain, get_subdomain_name, get_domain


def main():
    assert get_subdomain('http://www.google.com') == 'www.google.com'

    assert get_domain('http://google.com') == 'foo.foo'
    assert get_subdomain('http://foo.foo.google.com') == 'foo.foo.google.com'
    assert get_subdomain_name('http://foo.foo.google.com') == 'foo.foo'
    assert get_subdomain_name('htto://google.com') is None

if __name__ == '__main__':
    main()