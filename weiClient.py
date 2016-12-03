#! /usr/bin/env python  
# -*- coding: utf-8 -*-
'''
Created on 2016-8-24
@author: xiaocaiyidie
'''


from init import *
from PyQt4.QtCore import QTextCodec,QThread
from PyQt4.QtGui import QSystemTrayIcon,QApplication,QSplashScreen,QAction,QMenu,QPixmap
from common import app,Utils
from controller.chatClient import connectServer

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main(args):
    App = QApplication(args)
    splash = QSplashScreen(QPixmap("./view/winView/imgs/splash.png"));  splash.show()  # 启动动画
    App.processEvents()
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
    initProperty()       # 初始化
    app.Music.play()     # 开机音乐
    app.MainWin.show()   # 主窗口显示
    splash.finish(app.MainWin)
    createTray()         # 创建托盘
    # 调试状态不连线上接服务器
    if app.Debug:
        host = '114.215.209.164'
        # host = 'localhost'
        thread = Worker(None, host, 1234, app.AppUser, app.MainWin)  # 子进程
        thread.start()
        server= Server(None)  # 子进程
        server.start()
    # else:
    #     # 打开工具箱
    #     app._tool_.show()

    App.exec_()


#  托盘
def createTray():
    app.TrayIcon = QSystemTrayIcon(app.AppIcon, app.MainWin)
    app.TrayIcon.activated.connect(trayClick)
    app.TrayIcon.setToolTip("Geek Guide")
    app.TrayIcon.setContextMenu(createTrayMenu(app.TrayIcon,[1,3,4,5]))
    app.TrayIcon.show()

def trayClick(reason):
    if( reason == 3 ):
        if app.MainWin.isHidden():
            app.MainWin.show()
        app.MainWin.activateWindow()

# 托盘目录 根据角色判断
def createTrayMenu(trayIcon, role):
    trayIconMenu = QMenu()
    if 1 in role:
        action = QAction("主界面",trayIcon)
        action.triggered.connect(lambda:trayClick(3))
        trayIconMenu.addAction(action)
    if 2 in role:
        action = QAction("手动打印", trayIcon)
        action.triggered.connect(lambda: Utils.doPrint())
        trayIconMenu.addAction(action)
    if 3 in role:
        action = QAction("工具", trayIcon)
        action.triggered.connect(lambda: app._tool_.show())
        trayIconMenu.addAction(action)
    if 4 in role:
        action = QAction("执行", trayIcon)
        action.triggered.connect(lambda: app._robots_.run(0))
        trayIconMenu.addAction(action)
    if 5 in role:
        action = QAction("退出",trayIcon)
        action.triggered.connect(QApplication.instance().quit)
        trayIconMenu.addAction(action)

    return trayIconMenu

#  socket子进程多进程
class Worker(QThread):
    def __init__(self, parent=None, host='', port=505, user='', MainWin=''):
        QThread.__init__(self, parent)
        self.host = host
        self.port = port
        self.user = user
        self.MainWin = MainWin
    def __del__(self):
        self.exiting = True
        self.wait()
    def render(self):
        self.start()
    def run(self):
        # 子进程主体
        connectServer(self.host, self.port, self.user, self.MainWin)

#  本地服务子进程
class Server(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def __del__(self):
        self.exiting = True
        self.wait()
    def render(self):
        self.start()
    def run(self):
        # 子进程主体
        initServer()  # 初始化本地服务

if __name__ == "__main__":  
    main(sys.argv)