# coding=utf-8
from urlo.unicode import Url


class Unicode(unicode):

    def __str__(self):
        return self.encode('utf-8')

    #def __eq__(self, y):
    #    return super(Unicode, self).__eq__(y) if not isinstance(y, str) else str(self) == y


url = u'http://test.com/löl/aåd/🍺'

url_unicode = Unicode(u'%s' % url)
url_str = url_unicode.encode('utf-8')

assert str(url_unicode) == url_str

url = Url(url_str)
assert isinstance(url, unicode)