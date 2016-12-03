# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread
from pyquery import PyQuery as pq
from models import contact
import re
import time
'''
    工具箱进程
'''
#  解析html
def AnalysisHtml(html,MainWin):
    d = pq(html)
    qun_name = d('.group_name').text()
    num = 1
    all = len(list(item for item in d('.s_members_list ul li').items()))
    for li in d('.s_members_list ul li').items():
        data = {'qq': int(re.sub('\(|\)', '', li('.member_id').text())),
                'qun_name': qun_name,
                'role': 1 if len(li('.member_role').text()) > 0 else 0}  # 数据转化Dict
        print data
        try:
            contact.contact().insertVal(**data)
        except:
            pass
        MainWin.Progress.emit(num, all)  # 触发进度条
        num += 1

#  子进程
class ToolThread(QThread):
    def __init__(self, parent=None, html='',MainWin=None):
        QThread.__init__(self, parent)
        self.html = html
        self.MainWin = MainWin
    def __del__(self):
        self.exiting = True
        self.wait()
    def render(self):
        self.start()
    def run(self):
        # 子进程主体
        AnalysisHtml(self.html,self.MainWin)

'''
    微信机器人进程
'''
class WeixinThread(QThread):
    def __init__(self, parent=None,obj=None,num=0):
        QThread.__init__(self,parent)
        self.num = num
        self.obj = obj
    def __del__(self):
        self.exiting = True
        self.wait()
    def render(self):
        self.start()
    def run(self):
        self.obj.d = self.obj.connectAdb(self.num)
        self.obj.addFriendAct()  # 添加好友主程序
        self.obj.d.press.back()
        time.sleep(2)
        self.obj.d.press.home()
