#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: HanJieFeng
# Mail: hanjiefeng1987@126.com
# Created Time:  2018-12-12 10:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "yw-AUT",      #项目发布的名称
    version = "0.0.6",  #版本号，数值大的会优先被pip
    keywords = ("pip", "SICA","featureextraction"),
    description = "An feature extraction algorithm",
    long_description = "An feature extraction algorithm, improve the FastICA",
    license = "MIT Licence",

    url = "http://git.code.oa.com/yuewen-test/u2_stf_automator.git",     #项目相关文件地址，一般是github
    author = "HanJieFeng",
    author_email = "hanjiefeng1987@126.com",

    packages = find_packages(),
    package_data = {'ywAUT': ['project/steps/*.py', 'project/*.ini', 'project/testsuite/*.feature']},
    data_files=[('ywAUT', ['project/steps/*.py', 'project/*.ini', 'project/testsuite/*.feature'])],
    include_package_data = True,
    platforms = "any",
    install_requires = [
	"numpy",
	"stf-selector",
	"behave",
	"uiautomator2",
	"pillow",
	"configparser",
	"PyYAML",
	"weditor",
	]          #这个项目需要的第三方库
)
