#!/usr/bin/env python
# coding=utf-8
# Filename: setup.py
"""
jppy setup script.

"""
from setuptools import setup
from distutils.extension import Extension
import os
import subprocess as sp

VERSION = '2.0'

try:
    from Cython.Build import cythonize
    import numpy
except Exception:
    raise SystemExit("Please install Cython and Numpy:\n\n"
                     "    pip install cython numpy")

try:
    os.environ['JPP_DIR']
except KeyError:
    raise SystemExit("\n$JPP_DIR is not set. "
                     "You need to activate the JPP environment!")

try:
    ROOT_INC = sp.Popen(["root-config", "--incdir"],
                        stdout=sp.PIPE).communicate()[0].strip().decode()
    ROOT_LIB = sp.Popen(["root-config", "--libdir"],
                        stdout=sp.PIPE).communicate()[0].strip().decode()
    JPP_INC = os.environ['JPP_DIR'] + "/software"
    JPP_LIB = os.environ['JPP_LIB']
    # AANET_INC = os.environ['AANET_INC']           # not defined in all envs!
    AANET_INC = os.environ['AADIR']
    AANET_INC_EVT = os.path.join(AANET_INC, 'evt')
    AANET_INC_UTIL = os.path.join(AANET_INC, 'util')
    AANET_LIB = os.environ['AANET_LIB']
except OSError:
    raise ImportError("Cannot detect JPP!")


# compile_args = ['-g', '-std=c++11']  # ROOT6
compile_args = []


extensions = [
    Extension("jppy/*", ["jppy/*.pyx"],
              include_dirs=['src/', JPP_INC, AANET_INC, AANET_INC_EVT,
                            AANET_INC_UTIL, ROOT_INC, numpy.get_include()],
              library_dirs=[ROOT_LIB, JPP_LIB, AANET_LIB],
              libraries=['KM3NeTDAQROOT', 'evtROOT', 'aa', 'jaanetROOT',
                         'triggerROOT',
                         'Cint',    # ROOT5
                         # 'Cling',  # ROOT6
                         'pthread', 'dl', 'util', 'm',
                         'Core', 'RIO', 'Net', 'Hist', 'Graf',
                         'Graf3d', 'Tree', 'Rint', 'Matrix', 'Physics',
                         'MathCore', 'Gpad', 'Thread'],
              extra_compile_args=compile_args,
              language='c++',
              # extra_link_args=[]
              ),
]

setup(name='jppy',
      version=VERSION,
      url='http://git.km3net.de/tgal/jppy.git',
      description='Python bindings for JPP',
      author='Tamas Gal',
      author_email='tgal@km3net.de',
      packages=['jppy'],
      setup_requires=['setuptools>=24.3', 'pip>=9.0.1', 'cython', 'numpy'],
      install_requires=['cython', 'numpy'],
      ext_modules=cythonize(extensions, language='c++', gdb_debug=True),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          ],
      )
