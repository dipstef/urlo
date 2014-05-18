from distutils.command.build_py import build_py
from distutils.core import setup
import os
import shutil
from urlo.domain import tld_file_path, get_domain

VERSION = '0.1'

desc = """Collection of functions to handle url construction and parsing. Relies the top-level-domain extract
library to correctly parse url domain information."""

name = 'urlo'


class TldFileGenerator(build_py):

    def run(self):
        self.build_packages()

        if not os.path.exists(tld_file_path):
            print 'Generating: Tld File: '
            get_domain('www.google.com')

        build_file_path = os.path.join(self.build_lib, name, os.path.basename(tld_file_path))
        if not os.path.exists(build_file_path):
            shutil.move(tld_file_path, build_file_path)


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
      requires=['tldextract', 'unicoder']
)

