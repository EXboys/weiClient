# -*- coding: utf-8 -*-

from uiautomator import Device,Adb


# 获取设备总数
def allDevices():
    devices = Adb().devices().keys()
    return devices


# 连接设备
def connectDev(num):
    devices = allDevices()
    d = Device(devices[num])
    return d