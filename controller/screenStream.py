# -*- coding: utf-8 -*-
from connectDevices import *
from PyQt4.QtGui import *
import sys, os, time
from PyQt4.QtCore import *



class screenStream(QDialog):
    def __init__(self,num):
        super(screenStream, self).__init__()
        self.num = num
        self.all = allDevices()
        self.now = self.all[self.num]
        self.Xsize = 400
        self.Ysize = 650
        self.resize(self.Xsize, self.Ysize)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.Theading = screenTheading(self.num)
        self.connect(self.Theading, SIGNAL("updatescreen"), self.update)
        self.Theading.start()  # 线程开始

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.Xsize, self.Ysize, QPixmap(os.getcwd()+'\\'+str(self.num)+ "screen.png"))
        painter.end()


class screenTheading(QThread):
    def __init__(self,num):
        super(screenTheading, self).__init__()
        self.num = num
        self.d = connectDev(self.num)
    def run(self):
        while True:
            print 111
            self.d.screenshot(os.getcwd()+'\\'+str(self.num)+ "screen.png",0.2,10)
            self.emit(SIGNAL("updatescreen"))

if __name__=='__main__':
    app = QApplication(sys.argv)
    appadb = screenStream(0)
    appadb.show()
    app.exit(appadb.exec_())