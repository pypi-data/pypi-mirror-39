from distutils.core import setup
import sys

version = '2018.12.16'

setup(
  name = 'greater_context',
  packages = ['greater_context'], # this must be the same as the name above
  install_requires = (["strict_functions", "future"] if sys.version_info < (3,0) else ["strict_functions"]),
  version = version,
  description = 'A collection of useful python context managers to make life easier.',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/greater_context',
  download_url = 'https://github.com/CodyKochmann/greater_context/tarball/2018.12.16',
  keywords = ['greater_context', 'context', 'manager', 'logging', 'scope', 'control' ],
  classifiers = [],
)
