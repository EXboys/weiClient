# -*- coding: utf-8 -*-
import sys

from PyQt4.QtCore import QString,QUrl,SIGNAL,SLOT
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from threadLibs import ToolThread


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ToolKit(QWidget):

    def __init__(self,MainWin,parent = None):
        super(ToolKit, self).__init__(parent)
        self.url = 'http://127.0.0.1:5000/'
        self.MainWin = MainWin
        self.createLayout()
        self.createConnection()
        self.move(40, 80)
        self.webSettings = self.webView.settings()
        self.webSettings.setAttribute(QWebSettings.PluginsEnabled, True)
        self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.webSettings.setAttribute(QWebSettings.DeveloperExtrasEnabled,True)
        self.webView.page().linkClicked.connect(self.linkClicked)
        # self.show()

    def linkClicked(self, url):
        self.addressBar.setText(str(url)[20:-2])
        self.webView.load(url)

    def search(self):
        address = str(self.addressBar.text())
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
            url = QUrl(address)
            self.webView.load(url)

    def back(self):
        self.addressBar.setText(str(self.webView.history().backItem().url())[20:-2])
        self.webView.back()

    def forward(self):
        self.addressBar.setText(str(self.webView.history().forwardItem().url())[20:-2])
        self.webView.forward()

    # 后期优化
    def readContact(self):
        print '抓取中'
        # 此处必须装载到self，某则主界面会卡死
        self.thread = ToolThread(None,str(self.webView.page().mainFrame().toHtml()),self.MainWin)  # 子进程
        self.thread.start()

    def viewURL(self,url):
        self.addressBar.setText(url)
        self.webView.load(QUrl(url))

    def listContact(self):
        self.viewURL('http://127.0.0.1:5000')

    def createLayout(self):
        self.setWindowTitle("极客攻略工具箱")
        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8("../view/winView/imgs/icon.ico")), QIcon.Normal,
                       QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowOpacity(0.95)
        self.addressBar = QLineEdit(self.url)
        self.goButton = QPushButton(u"&刷新")
        self.forButton = QPushButton(u"&前进")
        self.backButton = QPushButton(u"&后退")
        self.getButton = QPushButton(u"&抓取")
        self.QQButton = QPushButton(u"&管理中心")
        bl = QHBoxLayout()
        bl.addWidget(self.backButton)
        bl.addWidget(self.addressBar)
        bl.addWidget(self.forButton)
        bl.addWidget(self.goButton)
        bl.addWidget(self.getButton)
        bl.addWidget(self.QQButton)
        self.webView = QWebView()
        layout = QVBoxLayout();layout.addLayout(bl);layout.addWidget(self.webView)
        self.setLayout(layout)
        self.webView.load(QUrl(self.url))


    def createConnection(self):
        self.connect(self.addressBar, SIGNAL('returnPressed()'), self.search)
        self.connect(self.addressBar, SIGNAL('returnPressed()'), self.addressBar, SLOT('selectAll()'))
        # 浏览
        self.connect(self.goButton, SIGNAL('clicked()'), self.search)
        self.connect(self.goButton, SIGNAL('clicked()'), self.addressBar, SLOT('selectAll()'))
        # 前进
        self.connect(self.forButton, SIGNAL('clicked()'), self.forward)
        self.connect(self.forButton, SIGNAL('clicked()'), self.addressBar, SLOT('selectAll()'))
        # 返回
        self.connect(self.backButton, SIGNAL('clicked()'), self.back)
        self.connect(self.backButton, SIGNAL('clicked()'), self.addressBar, SLOT('selectAll()'))
        # 抓取QQ号
        self.connect(self.getButton, SIGNAL('clicked()'), self.readContact)
        self.connect(self.getButton, SIGNAL('clicked()'), self.addressBar, SLOT('selectAll()'))
        # 获取QQ列表
        self.connect(self.QQButton, SIGNAL('clicked()'), self.listContact)
        self.connect(self.QQButton, SIGNAL('clicked()'), self.addressBar, SLOT('selectAll()'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browsers = ToolKit()
    browsers.show()
    sys.exit(app.exec_())