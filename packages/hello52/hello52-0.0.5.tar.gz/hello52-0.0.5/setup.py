#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "zhangyouliang"

PROJ_NAME = 'hello52'
PACKAGE_NAME = 'hello52'

PROJ_METADATA = '%s.json' % PROJ_NAME

import os,json,imp
here = os.path.abspath(os.path.dirname(__file__))

proj_info = json.loads(open(os.path.join(here,PROJ_METADATA),encoding='utf-8').read())

try:
    README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
except:
    README = ""

VERSION = imp.load_source('version',os.path.join(here,'src/%s/version.py' % PACKAGE_NAME)).__version__

from setuptools import setup,find_packages

setup(

    # pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    name = proj_info['name'],
    # version
    version = VERSION,

    author = proj_info['author'],
    author_email = proj_info['author_email'],
    url = proj_info['url'],
    license = proj_info['license'],

    long_description = README,

    description = proj_info['description'],
    keywords = proj_info['keywords'],
    #  需要安装的依赖
    install_requires =[
        'click>=3.3',
        'six>=1.5.0',
    ],
    # 需要打包的目录列表
    packages = find_packages('src'),
    package_dir = {'' : 'src'},

    test_suite = 'tests',

    platforms = 'any',
    zip_safe = True,
    #  启用清单文件 MANIFEST.in
    include_package_data = True,
    # 排除某些文件
    # exclude_package_date={'hello52':['.gitignore']},

    classifiers = proj_info['classifiers'],

    entry_points = {'console_scripts': proj_info['console_scripts']},


)


