# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    description='Roman numeral to/from converter scripts',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author='Eetu Lampsijärvi',
    url='https://github.com/Tulitomaatti/romanum',
    download_url='https://github.com/Tulitomaatti/romanum',
    author_email='eetu.lampsijarvi@helsinki.fi',
    version='0.1',
    install_requires=['nose'],
    packages=['romanum'],
    scripts=['bin/n2r', 'bin/r2n'],
    name='romanum',
    classifiers=[
        "Programming Language :: Python :: 2",
    ]
)
