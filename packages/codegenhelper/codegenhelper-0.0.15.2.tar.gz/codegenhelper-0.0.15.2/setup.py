#!/usr/bin/env python
from setuptools import setup, find_packages
name = "codegenhelper"

requires = [],

setup(
    name = name,
    version = '0.0.15.2',
    author = 'Zongying Cao',
    author_email = 'zongying.cao@dxc.com',
    description = 'utilities for code-engine.',
    long_description = """utilities for code-engine and their related projects""",
    url = 'https://github.com/cao5zy/codegen_helper',
    packages = ['codegenhelper'],
    install_requires = requires,
    license = 'Apache',
    classifiers = [
               'Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries',
           ],
)
