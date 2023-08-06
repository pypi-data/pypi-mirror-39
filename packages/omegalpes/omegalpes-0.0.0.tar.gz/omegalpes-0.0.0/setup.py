#! usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
OMEGAlpes installation script

:authors: B. DELINCHANT, S. HODENCQ, Y. MARECHAL, L. MORRIET,
          C. PAJOT, F. WURTZ
:license:
:version: 0.0.1
"""

from setuptools import setup, find_packages

# ------------------------------------------------------------------------------

# Module version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"

# ------------------------------------------------------------------------------


setup(

    name='omegalpes',
    # version=omegalpes.__version__,
    packages=["omegalpes"],
    author="B. DELINCHANT, S. HODENCQ, Y. MARECHAL, L. MORRIET, "
           "C. PAJOT, V. REINBOLD, F. WURTZ",
    # TODO: add the email adress
    # author_email='',
    description="OMEGAlpes is a linear energy systems modelling library",
    long_description=open('README.md').read(),
    install_requires=[
        "PuLP >= 1.6.8",
        "Matplotlib >= 2.2.2, <3.1",
        "Numpy >= 1.14.2, <1.16",
        "Pandas >= 0.22.0, <0.24"
    ],
    include_package_data=True,

    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
    ],

)
