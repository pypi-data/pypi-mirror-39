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
    version = "0.0.5",
    description = "Python command line application for mlgridengine.",
    long_description = long_descr,
    author = "RootLee",
    author_email = "ligen_thu@163.com",
    url = "https://github.com/ligengen/lazy-cmdline-tool",
    )
