#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import platform
import time
import json
import argparse
import shutil

__version__ = '0.0.5'
__dir__ = os.path.dirname(os.path.abspath(__file__))




def create_project(proectname):
    ywAUTpath = os.path.split(os.path.abspath(__file__))[0]+os.sep+"project"
    currentPath = os.getcwd()+os.sep
    projceDir = currentPath+proectname

    if os.path.exists(projceDir):
        print("项目"+proectname+"在当前目录已存在,请先删除!")
    else:
        shutil.copytree(ywAUTpath, projceDir)
        print("项目"+proectname+"新建成功！\n")


def main():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('-v', action='store_true',
                    help='查看当前版本')
    ap.add_argument('--setup','--name', type=str,
                    help='自定义名称创建测试工程')


    args = ap.parse_args()
    if args.setup:
        create_project(sys.argv[2])
        return

    if args.v:
        print(__version__)

if __name__ == '__main__':
    main()
