# coding=utf-8
from urlo.unquoted import params_url, exclude_parameters


def _build_params():
    # should always quote a url, otherwise the url parameter params mixes with the original url
    url = params_url(u'http://fdasdf.fdsfîășîs.fss', params={u'url': u'http://fdasdf.fdsfîășîs.fss/query&param=other'})
    assert url == u'http://fdasdf.fdsfîășîs.fss?url=http%3A//fdasdf.fdsfîășîs.fss/query%26param%3Dother'

def _exclude_params():
    url = exclude_parameters(u'http://test.com?foo=bar#1234', u'foo')
    assert url == u'http://test.com#1234'

def main():
    # _build_params()
    _exclude_params()


if __name__ == '__main__':
    main()
