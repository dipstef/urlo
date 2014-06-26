from urlo import UrlParse


def _is_valid(url):
    url = UrlParse(url)
    print url
    return url.is_valid()

assert _is_valid('http://asd.com/path')
assert _is_valid('http://192.168.1.1/path')
assert _is_valid('/path')
assert _is_valid('//google.com/test')
assert _is_valid('//google.com:81/test')

assert not _is_valid('http://asd/path')
assert not _is_valid('http://192.168.1/path')
assert not _is_valid('http:://192.168.1.1/path')