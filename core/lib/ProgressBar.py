# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class ProgressBar(QtGui.QWidget):
    trigger = QtCore.pyqtSignal(int, int)
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(u'工作进度')
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.move(40, 80)
        self.trigger.connect(self.getPercent)

    @QtCore.pyqtSlot(int, int)
    def getPercent(self, now,all):
        self.step = float(now)/all*100
        if self.step >= 100:
            self.step =100
        self.pbar.setValue(self.step)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    icon = ProgressBar()
    icon.trigger.emit(119, 600)
    icon.show()
    sys.exit(app.exec_())
