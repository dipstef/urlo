from urlo import Url

url = Url('http://www.google.com/query?s=foo&bar=1')
assert isinstance(url, str)

print url.parsed