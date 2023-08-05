#!/usr/bin/env python3

from setuptools import setup, find_packages   

setup(
    name = "paraparser",
    version = "1.0.0",  
    keywords = ("pip", "parameters", "parser"),
    description = "parameters process",
    long_description=open('README.rst').read(),
    license = "MIT Licence",

    url = "https://github.com/sky-y-zhang/paraparser.git",
    author = "Sky Zhang",
    author_email = "zyx474029625@126.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["six"] 
)

