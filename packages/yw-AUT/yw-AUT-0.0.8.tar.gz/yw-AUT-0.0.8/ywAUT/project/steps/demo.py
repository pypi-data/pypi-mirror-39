# coding=utf-8
from behave import *
import ywAUT.Globalvar as gl
d = gl.get_value('device')


@step("账号密码登陆")
def step_impl(context):
    d(resourceId="com.miui.home:id/icon_icon").click()
    d(description=u"2018年12月7日,农历冬月初一,星期五").click()
    d(description=u"2018年12月8日,农历冬月初二,星期六").click()



