#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Read config
Param:project path
Author: 韩杰峰
"""

import configparser
import os

class ReadConfig(object):
    def __init__(self, path):
        configPath = os.path.join(path, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='UTF-8')

    def get_method(self):
        value = self.cf.get("DEVICES", 'method')
        return value

    def get_server_url(self):
        value = self.cf.get("DEVICES", "server")
        return value

    def get_devices_ip(self):
        value = self.cf.get("DEVICES", "IP")
        return value.split('/')

    def get_devices_serial(self):
        value = self.cf.get("DEVICES", "serial")
        return value

    def get_apk_url(self):
        value = self.cf.get("APP", "apk_url")
        return value

    def get_pkg_name(self):
        value = self.cf.get("APP", "pkg_name")
        return value

    def get_testdata(self, name):
        value = self.cf.get("TESTDATA", name)
        return value.split('/')

    def get_server_token(self):
        value = self.cf.get("DEVICES", "token")
        return value

if __name__ == '__main__':
    print(ReadConfig().get_devices_serial())
