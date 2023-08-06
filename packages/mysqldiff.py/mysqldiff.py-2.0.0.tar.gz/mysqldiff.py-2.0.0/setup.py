# -*- coding: utf-8 -*-

# @Time    : 2018/12/20 12:45
# @Author  : zhoukang
# @File    : setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mysqldiff.py',
    version='2.0.0',
    description=(
        '一款轻量级数据库对比工具，同时支持新增表的默认数据导入！'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=["README.md"],
    author='Comclay',
    author_email='395525428@qq.com',
    license='Apache License 2.0',
    packages=find_packages(),
    platforms=["any"],
    url='https://github.com/Comclay/mysqldiff',
    install_requires=[
        'web.py',
        'MySQL-python'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License"
    ]
)
