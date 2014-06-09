from distutils.command.build_py import build_py
from distutils.core import setup
import logging

from urlo.domain import get_domain


VERSION = '0.1'

desc = """Collection of functions to handle url construction and parsing. Relies the top-level-domain extract
library to correctly parse url domain information."""

name = 'urlo'


def _configure_tld_logger():
    logger = logging.getLogger('tldextract')

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)


class TldFileGenerator(build_py):

    def run(self):
        _configure_tld_logger()
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