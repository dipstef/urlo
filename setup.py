from distutils.command.build_py import build_py
from distutils.core import setup

from urlo.domain import get_domain


VERSION = '0.1'

desc = """Collection of functions to handle url construction and parsing. Relies the top-level-domain extract
library to correctly parse url domain information."""

name = 'urlo'


class TldFileGenerator(build_py):

    def run(self):
        get_domain('http://google.com')
        build_py.run(self)



setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description='Url parsing and building',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=[name],
      platforms=['Any'],
      long_description=desc,
      cmdclass={'build_py': TldFileGenerator},
      package_data={'': ['hosts.txt']},
      requires=['tldextract', 'unicoder'])