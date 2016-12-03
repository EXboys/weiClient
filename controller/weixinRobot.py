# -*- coding: utf-8 -*-
from connectDevices import *
import time
import random
from models import contact,setting
from threadLibs import WeixinThread

class robots:
    def __init__(self):
        self.all = allDevices()
        self.setting = setting.setting()  # 初始化设置表model
        self.contact = contact.contact()  # 初始化联系表model
        self.per_day, self.per_add, self.sleep_time,self.next_exec,self.is_auto \
            = self.setting.getSetting()[0]   # 获取配置文件


    def run(self,num):
        self.nowDevice = self.all[num]
        devicesAddedToday = len(self.contact.deviceAdded(self.nowDevice))  # 当前设备今天添加总和
        if num <= len(self.all)-1 and devicesAddedToday<= self.per_day:
            try:
                self.thread = WeixinThread(None, self, num)
                self.thread.start()
            finally:
                return [self.next_exec,self.is_auto]  # 下次执行
        else:
            return False

    # 连接设备
    def connectAdb(self,num):
        devices = allDevices()
        self.d = Device(devices[num])
        return self.d

    # 打开软件
    def openSoft(self,name):
        self.d.press.home()
        self.d(text=str(name)).click()
        self.d.wait.update()
        self.rSleep()

    # 进入添加好友界面
    def toNewFriend(self):
        self.d(text="通讯录").click()
        self.rSleep()
        self.d(text="新的朋友").click()
        self.rSleep()
        if random.randint(0,1)==1:
            self.d(text="添加朋友").click()
            self.rSleep()

    def rSleep(self,times=1):
        start = self.sleep_time-1
        end   = self.sleep_time+1
        sec = random.randint(start,end)
        time.sleep(sec*times)

    # 添加好友
    def addFriend(self,qq):
        self.d(text="微信号/QQ号/手机号").click()
        self.rSleep()
        self.d(text='搜索').set_text(str(qq))
        self.rSleep()
        self.d(textContains='搜索:').click()
        self.rSleep()
        if self.d.exists(textContains='添加'):
            self.d(textContains='添加').click()
            self.rSleep()
            self.d(text='发送').click()
        if self.d.exists(textContains='用户不存在'):
            self.contact.noWeixin(qq)
        else:
            self.contact.weixinAdded(qq,self.nowDevice)
        self.rSleep()
        self.d.press.back()
        self.rSleep()
        self.d.press.back()
        self.rSleep(2)   # 二次添加延时

    # 添加好友主程序
    def addFriendAct(self):
        self.d.screen.on()  # 链接设备屏幕亮
        qq = self.contact.getQQ(self.per_add)  # 每次添加的QQ号
        print qq
        self.openSoft('微信')
        self.toNewFriend()  # 进入添加好友页面
        for item in qq:
            self.addFriend(item[0])





if __name__ == '__main__':
    # d = connectDev(0)
    # d.screen.on()
    # openSoft('微信')
    # toNewFriend()
    # # qq ='as392853771'
    # qq = '1122'
    # addFriend(qq)
    robots = robots()
    robots.connectAdb(0)
    robots.getScreenStream(0)

