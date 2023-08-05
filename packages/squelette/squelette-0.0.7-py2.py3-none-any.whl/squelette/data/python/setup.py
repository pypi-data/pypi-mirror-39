from setuptools import setup, find_packages
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()

with open(os.path.join(here, 'VERSION')) as version_file:
  version = version_file.read().strip()

setup(
  name='%(name)s',
  version=version,
  description='%(name)s - %(description)s',
  long_description=long_description,
  url='%(url)s',
  author='%(author)s',
  author_email='',
  license='%(license)s',
  packages=find_packages(),
  extras_require={
    'dev': ['pytest', 'tox']
  },
  entry_points={
    'console_scripts': [
      '%(name)s=%(name)s.%(name)s:hello',
    ],
  },
  scripts= ['bin/hello-%(name)s']
)
