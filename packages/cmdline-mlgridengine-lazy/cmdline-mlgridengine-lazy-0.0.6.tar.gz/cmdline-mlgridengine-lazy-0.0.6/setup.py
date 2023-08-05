# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup
import setuptools


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "cmdline-mlgridengine-lazy",
    packages = setuptools.find_packages(),
    entry_points = {
        "console_scripts": ['lazy=TerminalApi:lazy']
        },
    version = "0.0.6",
    description = "Python command line application for mlgridengine.",
    long_description = long_descr,
    author = "RootLee",
    author_email = "ligen_thu@163.com",
    url = "https://github.com/ligengen/lazy-cmdline-tool",
    install_requires=[
        'pytest==3.8.2',
        'colorama==0.3.9',
        'requests==2.18.4',
        'coverage==4.5.1',
        'pytz==2018.4',
        'click==7.0',
        'future-fstrings==0.4.4',
        'tokenize-rt==2.1.0',
        'mock==2.0.0',
        'pbr==4.3.0',
    ]
    )
