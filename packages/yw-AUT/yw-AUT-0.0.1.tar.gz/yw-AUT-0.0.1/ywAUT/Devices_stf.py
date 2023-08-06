#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
STF_Server, get devices, connect devices
Author: 韩杰峰
"""
import os
import logging
import time
from stf_selector.selector import Selector
from stf_selector.query import where
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
import re
import uiautomator2 as u2
import subprocess
from ReadConfig import ReadConfig
import requests

logger = logging.getLogger(__name__)
TinyDB.DEFAULT_STORAGE = MemoryStorage

s = Selector(url=ReadConfig().get_server_url(), token=ReadConfig().get_server_token())
s.load()


def devices_list():
    """获取平台所有设备"""
    devices = s.devices()
    return devices


def ready_devices():
    """查找标记为ready的设备"""
    devices = s.find(where('ready') == True).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def online_devices():
    """查找online 的设备"""
    devices = s.find(where('present') == True).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def model_devices(model):
    """查找特定型号的设备"""
    devices = s.find(where('model') == model).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def brand_devices(brand):
    """查找特定品牌的设备"""
    devices = s.find(where('brand') == brand).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def sdk_devices(sdk):
    '''查找特定SDK的设备'''
    devices = s.find(where('sdk') == sdk).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def version_devices(version):
    '''查找特定SDK的设备'''
    devices = s.find(where('version') == version).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def serial_devices(serial):
    '''查找特定serial的设备'''
    devices = s.find(where('serial') == serial).devices()
    if len(devices) > 0:
        return devices
    else:
        return False


def get_remoteurl(serial):
    '''查找特定serial的设备'''
    devices = s.find(where('serial') == serial).devices()
    if len(devices) > 0:
        return devices[0]['remoteConnectUrl']
    else:
        return False


'''
连接已插线设备
'''


def connect_usb_stf_devices():
    '''get the devices usb connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('连接USB设备，设备名 %s' % valid_serials)
        devices_list = []
        for i in valid_serials:
            try:
                device = u2.connect_usb(i)
                # device.healthcheck()
                if device.alive:
                    dict_tmp = device.device_info
                    devices_list.append(dict_tmp)
                else:
                    print('设备 %s 不可用,请检查usb链接状态!' % i)
            except Exception as e:
                print('返回错误: %s\n 设备 %s 不可用,请检查usb链接状态!' % (e, i))
        return device
    if len(valid_serials) == 0:
        print("未发现可用的USB设备,请检查设备连接情况!")


'''
连接USB指定serial设备
'''


def connect_serial_usb_stf_devices(serial):
    '''
    adb connect
    '''

    remote_url = get_remoteurl('4b89b1ce9905')


    '''get the devices usb connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('连接USB设备，设备名 %s' % serial)
        devices_list = []
        try:
            device = u2.connect_usb(remote_url)
            device.healthcheck()
            if device.alive:
                dict_tmp = device.device_info
                devices_list.append(dict_tmp)
            else:
                print('设备 %s 不可用,请检查usb链接状态!' % serial)
        except Exception as e:
            print('返回错误: %s\n 设备 %s 不可用,请检查usb链接状态!' % (e, serial))
        return device
    if len(valid_serials) == 0:
        print("未发现可用的USB设备,请检查设备连接情况!")


'''
STF打开remote
'''


def open_stf_remote(serial):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + ReadConfig().get_server_token()
    }
    data = {
        'serial': serial
    }
    r = requests.post('http://10.97.190.152:7100/api/v1/user/devices', json=data, headers=headers)
    return r


'''
STF关闭remote
'''


def close_stf_remote(serial):
    headers = {
        'Authorization': 'Bearer ' + ReadConfig().get_server_token()
    }
    r = requests.request('DELETE', 'http://10.97.190.152:7100/api/v1/user/devices/' + serial,
                         headers=headers)
    return r


if __name__ == '__main__':
    # print(len(online_devices()))
    #print(model_devices(' 6T'))

    #open_stf_remote('4b89b1ce9905')
    #time.sleep(20)

    remote_url = get_remoteurl('4b89b1ce9905')
    print("before:"+str(remote_url))
    open_stf_remote('4b89b1ce9905')
    s = Selector(url=ReadConfig().get_server_url(), token=ReadConfig().get_server_token())
    s.load()
    remote_url = get_remoteurl('4b89b1ce9905')
    print("after:"+str(remote_url))
    print(serial_devices('4b89b1ce9905'))
    os.system('adb connect '+remote_url)
    time.sleep(10)
    connect_serial_usb_stf_devices('4b89b1ce9905')
    close_stf_remote('4b89b1ce9905')