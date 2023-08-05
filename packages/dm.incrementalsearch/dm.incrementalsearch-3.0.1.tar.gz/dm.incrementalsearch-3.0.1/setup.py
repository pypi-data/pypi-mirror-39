#       $Id: setup.py,v 1.2 2018/11/28 09:36:06 dieter Exp $
from os import environ
from os.path import join, exists, abspath
from sys import exit
from distutils.core import Extension

from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup, Extension
  setupArgs = dict(
      setup_requires=["BTrees", "persistent"],
      install_requires=["BTrees", "persistent"],
      include_package_data=True,
      namespace_packages=['dm'],
      zip_safe=False, # to let the tests work
      )
except ImportError:
  # use distutils
  from distutils import setup
  from distutils.core import Extension
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'incrementalsearch')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()


# Auxiliary class taken from `setup.py` of `BTrees`.
class ModuleHeaderDir(object):
  def __init__(self, require_spec, where='..'):
    # By default, assume top-level pkg has the same name as the dist.
    # Also assume that headers are located in the package dir, and
    # are meant to be included as follows:
    #    #include "module/header_name.h"
    self._require_spec = require_spec
    self._where = where
  def __str__(self):
    from pkg_resources import require
    from pkg_resources import resource_filename
    require(self._require_spec)
    path = resource_filename(self._require_spec, self._where)
    return abspath(path)


setup(name = "dm.incrementalsearch",
      version=pread('VERSION.txt').split('\n')[0],
      description='An efficient low level search execution engine on top of ZODB.BTrees.',
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: ZODB',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: Implementation :: CPython",
        'Programming Language :: C',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='https://pypi.org/project/dm.incrementalsearch',
      packages=['dm', 'dm.incrementalsearch', 'dm.incrementalsearch.tests'],
      keywords='search, efficient, ZODB, incremental, BTrees',
      license='BSD (see "dm/incrementalsearch/LICENSE.txt", for details)',
      ext_modules = [
         Extension("dm.incrementalsearch._isearch",
            [join('dm', 'incrementalsearch', f)
             for f in ("_isearch.c", "_isearch_int.c", "_isearch_obj.c", "_isearch_long.c")],
            include_dirs = [ModuleHeaderDir("BTrees"), ModuleHeaderDir("persistent")],
            ),
         ],
      **setupArgs
      )
