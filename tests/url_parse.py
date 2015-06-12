# coding=utf-8
from urlo import UrlParse


def _iri_parse_test():
    iri = UrlParse(u'http://fdasdf.fdsfîășîs.fss/ăîăî')

    assert iri.scheme == u'http'
    assert iri.host == u'fdasdf.fdsfîășîs.fss'
    assert iri.path == u'/ăîăî'


if __name__ == '__main__':
    _iri_parse_test()
