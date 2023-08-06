#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################
# File Name: setup.py
# Author: YuFeng
# Mail: 125213990@qq.com
# Created Time:  2018-12-15 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "DZLtest",      #这里是pip项目发布的名称
    version = "0.1.0",  #版本号，数值大的会优先被pip
    keywords = ("pip", "SICA","test"),
    description = "A test example",
    long_description = "blabla",
    license = "MIT Licence",

    url = "https://github.com/Tangxiaodou/test",     #项目相关文件地址，一般是github
    author = "YuFeng",
    author_email = "1252131990@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)
