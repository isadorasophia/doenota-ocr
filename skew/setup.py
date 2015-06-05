#!/usr/bin/python
 
from distutils.core import setup
from distutils.extension import Extension
 
setup(name="Skew",
    ext_modules=[
        Extension("skew", ["skew.cpp"],
        libraries = ["boost_python"])
    ])