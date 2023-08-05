from setuptools import setup, find_packages
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()

with open(os.path.join(here, 'VERSION')) as version_file:
  version = version_file.read().strip()

setup(
  name='squelette',
  version=version,
  description='squelette - skeleton generator',
  long_description=long_description,
  url='http://appliedstochastics.com',
  author='Ajay Khanna',
  author_email='',
  license='MIT',
  packages=find_packages(),
  package_data={'squelette': ['data/python/*', 'data/python/.gitignore',
    'data/python/0/*', 'data/python/bin/*', 'data/python/template/*',
    'data/python/tests/*']},
  extras_require={
    'dev': ['pytest', 'tox']
  },
  scripts=['bin/squelette']
)
