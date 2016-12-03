#! /usr/bin/env python  
# -*- coding: utf-8 -*-
'''
Created on 2016-8-27

@author: xiaocaiyidie
'''
import os
import sys
import time
import webbrowser

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from pyquery import PyQuery as pq

from Dialog import Dialog
from RoundWindow import RoundWindow
from ProgressBar import ProgressBar
from common import Utils,app
from controller.printerClient import Printer


reload(sys)
sys.setdefaultencoding('utf8')


class Window(RoundWindow):
    DialogWindow=None
    ProgressWindow = None
    ToolWindow = None
    Notification = pyqtSignal(str, int)  # 调用Notification
    Progress = pyqtSignal(int, int)      # 调用进度
    def __init__(self,url,width,height,windowType=0,handleMethod=""):
        super(Window, self).__init__()
        self.resize(width,height)
        self.round()

        # window窗口设置
        point = Utils.getDesktopCenterPoint(self)
        self.move(point["x"]*(float(3)/4)+point["x"],80)
        self.setWindowTitle(app.AppTitle)
        self.setWindowIcon(app.AppIcon)
        self.setWindowOpacity(app.Opacity)

        # 网页窗口配置
        self.webview = QWebView(self)
        self.webview.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, app.Debug)
        self.webview.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.webview.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.webview.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webview.settings().setLocalStoragePath(app.HomeDir + "/data")
        self.webview.settings().setDefaultTextEncoding("utf-8")

        # 定制画布大小，一般为固定大小
        self.webview.setGeometry(1,1,self.width()-2,self.height()-2)
        self.webview.setStyleSheet("QWebView{background-color: rgba(123, 104, 238, 100%); }")
        self.webview.page().networkAccessManager().setCookieJar(app.CookieJar)
        self.webview.page().mainFrame().javaScriptWindowObjectCleared.connect(self.setJavaScriptObject)
        self.webview.page().linkClicked.connect(self.linkClicked)

        # 提醒窗口
        self.Notification.connect(self.refreshUrl)
        # 进度条
        self.Progress.connect(self.showProgress)

        # 定时器，socket失败的备选方案,定时检索打印
        # self.timer = QTimer()
        # self.connect(self.timer, SIGNAL("timeout()"), Utils.doPrint)
        # self.timer.start(120000)
        # 定时器，机器人是否自动执行
        self.robotTimer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.runRobots)

        # self.webview.page().featurePermissionRequested.connect(self.permissionRequested)
        self.webview.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.handleMethod= handleMethod
        self.subUrl=url
        self.windowType=windowType
        self.url = QUrl.fromLocalFile(app.ViewDir+"window.html")
        self.webview.load(self.url)
    
    # def permissionRequested(self,frame,feature):
    #    self.webview.page().setFeaturePermission(frame, feature, QWebPage.PermissionGrantedByUser)

    def linkClicked(self,url):
        # url =  str(url)[20:-2]
        # # print url
        # self.webview.page().mainFrame().evaluateJavaScript('loadFrame("%s")' % (url))
        # self.webview.load(url)
        # 使用默认浏览器打开
        webbrowser.open(url.toString())

    def setJavaScriptObject(self):
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_window_", self)
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_notifications_", app._notifications_)
        self.webview.page().mainFrame().addToJavaScriptWindowObject("_tool_", app._tool_)

    @pyqtSlot(str, int)   # 提示
    def refreshUrl(self, url='', type=0):
        if url <> '':
            webbrowser.open(url, 0, False)
        if type == 1:
            app._notifications_.showNotification("新订单提醒", "osc_tweet_notice",
                                                 "您有新的订单！请及时处理", 10000)
        elif type == 0:
            app._notifications_.showNotification("暂时没有订单","osc_tweet_notice",
                                                 "暂时没有订单，请继续努力",
                                                 10000)
        elif type == 2:
            app._notifications_.showNotification("已经完成", "osc_tweet_notice",
                                                 "主人，您交代的工作已经完成哦", 10000)
        else:
            pass


    @pyqtSlot(int, int)   # 进度条程序
    def showProgress(self,now,all):
        if self.ProgressWindow == None:
            self.ProgressWindow = ProgressBar()
            self.ProgressWindow.show()
            qe = QEventLoop()
            qe.exec_()
        else:
            self.ProgressWindow.show()
        self.ProgressWindow.getPercent(now, all)
        if now == all:
            self.ProgressWindow.hide()
            app._notifications_.showNotification("极客宝宝", "osc_tweet_notice",
                                                 "主人，您的数据已经下载完成哦！！！", 30000)


    # 如有登录功能可以实现自动登录
    # def cancelAutoLogin(self):
    #     self.webview.page().mainFrame().evaluateJavaScript("window.localStorage.autoLogin='false';")
        
    @pyqtSignature("",result="QString")
    def getUrl(self):
        return self.subUrl
    
    @pyqtSignature("",result="QString")
    def getHandleMethod(self):
        return self.handleMethod
    
    @pyqtSignature("",result="int")
    def getWindowType(self):
        return self.windowType

    # 对话窗口
    @pyqtSignature("")
    def openDialogWindow(self):
        if self.DialogWindow!=None:
            self.DialogWindow.show()
            return 
        self.DialogWindow = Dialog()
        self.DialogWindow.show()
        qe = QEventLoop()
        qe.exec_()

    # 工具窗口
    @pyqtSignature("")
    def openToolWindow(self):
        if self.ToolWindow != None:
            self.ToolWindow.show()
            return
        self.ToolWindow = app._tool_
        self.ToolWindow.hide()
        self.ToolWindow.show()
        qe = QEventLoop()
        qe.exec_()

    # 微信机器人
    @pyqtSignature("")
    def runRobots(self):
        allDevices = app._robots_.allDevices()
        for i in range(len(allDevices)):
            # 添加新粉丝
            self.message = app._robots_.run(i)
            print self.message
            if self.message == False:
                app._notifications_.showNotification("极客提醒","osc_tweet_notice",
                                                    "ID 为({})的设备不可用或者今日已达上限！！！".format(allDevices[i]),
                                                     30000)
            else:
                app._notifications_.showNotification("极客提醒","osc_tweet_notice",
                                                    "ID 为({})的设备正在执行此次工作，请确认！！！".format(allDevices[i]),
                                                     30000)
                time.sleep(10)
                if self.message[1] == True:  # 是否自动执行
                    self.robotTimer.start(self.message[0] * 1000)
                    app._notifications_.showNotification("极客提醒", "osc_tweet_notice",
                                                        "ID 为({})的设备每隔{}秒自动执行，请确认！！！".
                                                         format(allDevices[i],self.message[0]),30000)
                else:
                    self.robotTimer.stop()
                    app._notifications_.showNotification("极客提醒", "osc_tweet_notice",
                                                         "ID 为({})的设备已取消自动执行，请确认！！！".
                                                         format(allDevices[i], self.message[0]), 30000)


    @pyqtSignature("QString,QString")
    def windowAlert(self,title,text):
        QMessageBox.information(self,title,text)

    @pyqtSignature("")
    def jsPrinterAuto(self):
        html = pq(str(self.webview.page().currentFrame().toHtml()).decode('utf-8')).html() # 注意打印字符格式
        print html
        try:
            for i in range(3):
                # html = Printer().printFormat(html)
                p = "defaultPrinter"  # 打印机名称
                Printer().printing(p, html)
                time.sleep(1)
        except:
            pass

    @pyqtSignature("")
    def fullScreen(self):
        self.fullScreen()

    @pyqtSignature("")
    def minimize(self):
        if(self.windowType==0):
            self.hide()
        else:
            self.showMinimized()
    
    @pyqtSignature("")
    def quit(self):
        if(self.windowType==0):
            res = QMessageBox.question(self, "关闭提示", "你点击了关闭按钮\n你是想“最小化”还是“退出”？",
                                       "最小化", "退出","取消",0,2)
            if(res==1):
                QApplication.instance().quit()
            elif(res==0):
                self.hide()
        else:
            self.close()
    
    @pyqtSignature("int,int")
    def moveTo(self,offsetX,offsetY):
        self.move(self.x()+offsetX,self.y()+offsetY)
    
    @pyqtSignature("QString,int,int,int,QString")
    def open(self,url,width,height,windowType,handleMethod):
        win = Window(url,width,height,windowType,handleMethod)
        win.show()
        qe = QEventLoop()
        qe.exec_() 
    
    @pyqtSignature("",result="QString")
    def getSkinItem(self):
        path = app.ViewDir+"/imgs/skin/"
        html = ["<ul class='skin-imgs'>"]
        for file in os.listdir(path):
            html.append("<li>")
            html.append("<img  src='./imgs/skin/"+file+"'/>")
            html.append("</li>")
        html.append("</ul>")
        return ''.join(html)