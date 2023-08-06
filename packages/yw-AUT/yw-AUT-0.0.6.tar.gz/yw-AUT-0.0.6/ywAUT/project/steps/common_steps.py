# coding=utf-8
import os
from behave import *
from ywAUT.Driver import Driver
import ywAUT.Globalvar as gl
'''
    1. 初始化启动driver
    2. 连接设备
    3. 扩大driver作用域
    4. 引导配置文件
'''
driver = Driver(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))
d = driver.connect_device()
gl._init()
gl.set_value('device', d)


@step("安装app")
def step_impl(context):
    driver.app_install()


@step("打开app")
def step_impl(context):
    driver.app_start()


@step("关闭app")
def step_impl(context):
    driver.app_stop()
    driver.close_remote()


@step('点击包含"{key_value}"的文本')
def step_impl(context, key_value):
    d(text=key_value).click()


@step('点击包含"{key_value}"的按钮')
def step_impl(context, key_value):
    d(text=key_value).click()


@step('页面包含"{key_value}"')
def step_impl(context, key_value):
    assert d(text=key_value).wait(timeout=20)


@step('页面不包含"{key_value}"')
def step_impl(context, key_value):
    assert not d(text=key_value).wait(timeout=20)


@step('向上滑动到"{key_value}"处')
def step_impl(context, key_value):
    d(scrollable=True).scroll.to(text=key_value)


@step('向左滑动到"{key_value}"处')
def step_impl(context, key_value):
    d(scrollable=True).scroll.horiz.forward(steps=100)


@step('向"{forward}"滑动(\d+)次')
def step_impl(context, forward, time):
    for i in range(int(time)):
        if forward == '左':
            d.swipe(370, 370, 70, 370, 0)
        elif forward == '右':
            d.swipe(70, 370, 370, 370, 0)
        elif forward == '上':
            d.swipe(370, 170, 370, 570, 0)
        elif forward == '下':
            d.swipe(370, 570, 370, 170, 0)

