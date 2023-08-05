import os

_root_d = os.path.join(os.path.dirname(__file__))
_data_d = os.path.join(_root_d, 'data')

with open(os.path.join(_root_d, 'VERSION')) as _version_file:
  __version__ = _version_file.read().strip()
