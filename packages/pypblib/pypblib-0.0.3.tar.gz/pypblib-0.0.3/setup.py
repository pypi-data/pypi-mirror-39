#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, Extension
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup, Extension
    HAVE_SETUPTOOLS = False

import glob
import os.path

from pypblib import VERSION_STR

# comma separated list of names
AUTHORS = 'Carlos Ansótegui, Toni Pacheco, Josep Pon'

# comma separated list of emails, following authors ordering
EMAILS = ''

# Short description
DESCRIPTION = ""

# Long description
with open('README.rst') as f:
    README = f.read()

# Requirements
with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()


# Additional keyword arguments
if HAVE_SETUPTOOLS:
    kwargs = {
        # 'entry_points': {
        #    'console_scripts': ['dgga = pydgga.__main__:main']
        # },
        'install_requires': REQUIREMENTS,
    }
else:
    kwargs = {
        # 'scripts': ['scripts/dgga']
    }

# Extensions
##############################################################################

EXTENSIONS = []

# PBLib
#######

PBLIB_ROOT_DIR = os.path.join('External', 'pblib')
PBLIB_ENC_DIR = os.path.join(PBLIB_ROOT_DIR, 'encoder')

PBLIB_SRCS = glob.glob(os.path.join(PBLIB_ROOT_DIR, '*.cpp'))
PBLIB_SRCS.extend(glob.glob(os.path.join(PBLIB_ENC_DIR, '*.cpp')))

PBLIB_MOD_ROOT_DIR = os.path.join('Modules/pblib')
PBLIB_MOD_SRCS = glob.glob(os.path.join(PBLIB_MOD_ROOT_DIR, '*.cpp'))
PBLIB_MOD_SRCS.extend(PBLIB_SRCS)

EXTENSIONS.append(
    Extension('pypblib.pblib', sources=PBLIB_MOD_SRCS,
              include_dirs=[PBLIB_ROOT_DIR, PBLIB_MOD_ROOT_DIR],
              libraries=[], extra_compile_args=['-std=c++11'])
)


##############################################################################

setup(
    name='pypblib',
    version=VERSION_STR,
    description=DESCRIPTION,
    long_description=README,
    author=AUTHORS,
    author_email=EMAILS,
    url="https://arcadia.hardlog.udl.cat/hlog-tools/pypblib",
    license="",
    keywords='PBLib Pseudo-Boolean CNF PB',
    packages=['pypblib'],
    ext_modules=EXTENSIONS,
    platforms='Linux',
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    **kwargs
)
