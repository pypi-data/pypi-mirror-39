#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : setup.py
Author : Zerui Qin
CreateDate : 2018-12-06 10:00:00
LastModifiedDate : 2018-12-06 10:00:00
Note : 打包上传PyPi
"""

import setuptools

with open('README.md') as fp:
    long_description = fp.read()

setuptools.setup(
    name='watero-go',
    version='0.1',
    author='Clever Moon',
    author_email='qzr19970105@live.com',
    description='采集节点数据并上报Watero Center，同时接收Watero Center推送的控制信息',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Qinnnnnn/Watero_Go',
    packages=setuptools.find_packages(),
    install_requires=['requests', 'psutil'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
