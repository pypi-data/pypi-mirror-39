#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: HanJieFeng
# Mail: 26736548@qq.com
# Created Time:  2018-12-06
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "yw-AUT",      #这里是pip项目发布的名称
    version = "0.0.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "ywAUT","featureextraction"),
    description = "yw-stf-behava-u2",
    long_description = "An feature extraction algorithm, improve the automator",
    license = "MIT Licence",

    url = "http://git.code.oa.com/yuewen-test/u2_stf_automator.git",#项目相关文件地址，一般是github
    author = "HanjieFeng",
    author_email = "26736548@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "behave",
        "stf-selector",
        "uiautomator2",
        "pillow",
        "configparser",
        "PyYAML",
	"weditor"
    ]
)
