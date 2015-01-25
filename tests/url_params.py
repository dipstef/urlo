# coding=utf-8
from urlo.unquoted import params_url


def main():
    # should always quote a url, otherwise the url parameter params mixes with the original url
    url = params_url(u'http://fdasdf.fdsfîășîs.fss', params={u'url': u'http://fdasdf.fdsfîășîs.fss/query&param=other'})
    print url

if __name__ == '__main__':
    main()