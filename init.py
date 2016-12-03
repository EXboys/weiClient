#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016-11-22
@author: xiaocaiyidie
'''

import json
import mp3play
from os import getcwd
from PyQt4.QtGui import QIcon
from common import app
from core.lib.Notification import NotificationPresenter
from PyQt4.QtNetwork import QNetworkCookieJar
from core.lib.Window import Window
from controller import toolKit
from controller.weixinRobot import robots
import sys,os
import thread
import subprocess

def initServer():
    try:
        subprocess.call('taskkill /f /t /im appServer.exe')
    except Exception, e:
        pass
    thread.start_new_thread(subprocess.call(os.getcwd()+'/appServer.exe'))


def initProperty():
    manifest = json.load(file('./view/app.json'))
    app.AppTitle = manifest['name'] if manifest['name'] else app.AppTitle
    app.AppUser = manifest['user'] if manifest['user'] else app.AppUser
    app.Debug = manifest['debug'] if manifest['debug'] else app.Debug
    app.HomeDir = getcwd()
    app.Template = manifest['win'] if manifest['win'] else app.Template
    app.App = manifest['app'] if manifest['app'] else app.App
    app.ViewDir = app.HomeDir+'/view/'+app.Template+'/'
    app.AppDir  = app.HomeDir+'/view/'+app.App+'/'
    app.AppIcon = QIcon(app.ViewDir + (manifest['ico'] if manifest['ico'] else app.AppIcon))
    #主页面配置
    app.MainSrc = manifest['main']['url'] if manifest['main']['url'] else app.MainSrc
    app.WinWidth = manifest['main']['width'] if manifest['main']['width'] else app.WinWidth
    app.WinHeight = manifest['main']['height'] if manifest['main']['height'] else app.WinHeight
    app.Opacity = manifest['opacity'] if manifest['opacity'] else app.Opacity
    #对话框配置
    app.DialogSrc = manifest['dialog']['url'] if manifest['dialog']['url'] else app.DialogSrc
    app.DialogCon = manifest['dialog']['content'] if manifest['dialog']['content'] else app.DialogCon
    app.DialogWidth = manifest['dialog']['width'] if manifest['dialog']['width'] else app.DialogWidth
    app.DialogHeight = manifest['dialog']['height'] if manifest['dialog']['height'] else app.DialogHeight
    app.DialogOpacity = manifest['dialog']['opacity'] if manifest['dialog']['opacity'] else app.DialogOpacity

    app.Music = mp3play.load('./view/winView/assets/notify.mp3')

    # 各类初始化
    app._notifications_ = NotificationPresenter()
    app.CookieJar = QNetworkCookieJar()
    app.MainWin = Window(app.MainSrc, app.WinWidth, app.WinHeight)  # 打开窗口
    app._tool_ = toolKit.ToolKit(app.MainWin)
    app._robots_ = robots()





