#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create Driver
Author: 韩杰峰
"""

import sys
from Devices import *
from Devices_s import *
from ReadConfig import ReadConfig
import uiautomator2.ext.htmlreport as htmlreport

reload(sys)
sys.setdefaultencoding('utf8')


class Driver:
    # 启动服务
    def __init__(self):
        """获取ATX服务连接"""
        self.s = STF_Server()

    """连接设备
       USB:连接本机设备
       IP:连接无线设备平台设备
    """

    def connect_device(self):
        global d
        if ReadConfig().get_method() == "USB":
            serial_id = ReadConfig().get_devices_serial()
            if serial_id:
                print('指定执行设备'+serial_id)
                d = self.s.connect_serial_usb_stf_devices(serial_id)
            else:
                print('自动选择adb devices首个设备')
                d = self.s.connect_usb_devices()
        # else:
        #     if len(ReadConfig().get_devices_ip()) == 0:
        #         d = connect_devices_online_ip(self.s.online_devices()[0]['ip'])
        #     else:
        #         d = get_devices_config_ip()
        """健康检查"""
        if d:
            d.healthcheck()
            hrp = htmlreport.HTMLReport(d)
            hrp.patch_click()
            return d
        else:
            print("连接设备失败!")

    def app_install(self):
        """安装APP，传入url"""
        d.app_install(ReadConfig().get_apk_url())


    def app_start(self):
        """启动APP"""
        d.app_stop_all()
        d.app_start(ReadConfig().get_pkg_name())


    def app_stop(self):
        """关闭APP"""
        d.app_stop(ReadConfig().get_pkg_name())
        """执行完成，挂起u2亮屏进程，防止熄屏断网"""
        d.shell('am start -n com.github.uiautomator/.IdentifyActivity')


    def unlock_device(self):
        """unlock.apk install and launch"""
        pkgs = re.findall('package:([^\s]+)', d.shell(['pm', 'list', 'packages', '-3'])[0])
        if 'io.appium.unlock' in pkgs:
            d.app_start('io.appium.unlock')
            d.shell('input keyevent 3')
        else:
            #  appium unlock.apk 下载安装
            print('installing io.appium.unlock')
            d.app_install('https://raw.githubusercontent.com/ATX-GT/master/apk/unlock.apk')
            d.app_start('io.appium.unlock')
            d.shell('input keyevent 3')
