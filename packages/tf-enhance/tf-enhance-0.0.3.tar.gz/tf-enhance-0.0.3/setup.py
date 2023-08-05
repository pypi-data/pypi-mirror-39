#!/usr/bin/python
# -*- coding=UTF-8 -*-
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__name__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_desc = f.read()

setup(name='tf-enhance',
      version='0.0.3',
      description='An easy enhancement framework for TensorFlow.',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      url='https://github.com/LovelyLazyCat/tf-enhance',
      author='LazyCat',
      author_email='lazycat7703@gmail.com',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.6'],
      packages=find_packages(exclude=['tfenhance']))
