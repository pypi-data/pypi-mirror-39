#!/usr/bin/env python

from setuptools import setup
import os
import codecs
import re

#Copied from wheel package
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.dirname(__file__), 'graphstat', '__init__.py'),
                 encoding='utf8') as version_file:
    metadata = dict(re.findall(r"""__([a-z]+)__ = "([^"]+)""", version_file.read()))

setup(name='graphstat',
      version=metadata['version'],
      description='Graph collection in several forms.',
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        ],
      author='Masakazu Matsumoto',
      author_email='vitroid@gmail.com',
      url='https://github.com/vitroid/graphstat/',
      keywords=['graphstat','graph','statistics'],
      license='MIT',
      packages=['graphstat',
                ],
      install_requires=['numpy', 'networkx>=2',],
      )

