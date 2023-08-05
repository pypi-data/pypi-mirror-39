#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs

__author__ = "xuzhao"
__email__ = "contact@xuzhao.xin"
__file__ = "setup.py"
__description__ = ""
__created_time__ = "2018/11/30 16:39"

import setuptools

with codecs.open('README.md', 'r', encoding='utf8') as fp:
    long_description = fp.read()

setuptools.setup(name='xuzhao-markdown-editor',
                 version='1.1',
                 description='xuzhao markdown editor',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='xuzhao',
                 author_email='markdown@felinae.net',
                 url='https://markdown.felinae.net',
                 keywords='django markdown editor editormd',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 install_requires=[],
                 include_package_data=True,
                 classifiers=(
                     "Programming Language :: Python",
                     "Development Status :: 4 - Beta",
                     "Operating System :: OS Independent",
                     "License :: OSI Approved :: Apache Software License",
                     "Framework :: Django"
                 ))