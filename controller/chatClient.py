# -*- coding: utf-8 -*-
import random
import socket
import sys
import threading
import time

import requests

import core.vendor.requestByURL
from controller.printerClient import Printer
from core.vendor.header import *

reload(sys)
sys.setdefaultencoding("utf-8")

class socketThread(threading.Thread):
    def __init__(self, fun_id, s, user, MainWin):
        super(socketThread, self).__init__()
        self.fun_id = fun_id
        self.s = s
        self.user=user
        self.MainWin = MainWin
        self.startTime = time.time()

    def run(self):
        if self.fun_id == 1:
            self.receive()
        else:
            self.sendMessage()

    '''
        接受信息
    '''
    def receive(self):
        while True:
            try:
                buf = self.s.recv(1024)
                print buf
                if len(buf):
                    # print "he say: "+buf.decode('utf-8')
                    # print 'receive'
                    # 将接收的消息语音读出
                    # try:
                    #     import pythoncom
                    #     pythoncom.CoInitialize()
                    #     win32com.client.Dispatch("SAPI.SpVoice").Speak(str(buf).decode('utf-8'))
                    # except:
                    #     pass
                    try:
                        buf = buf.replace('\r\n','')
                        if str(buf)==str('new'):
                            time.sleep(0.5)
                            URL = 'http://yii.kuaxiango.com/backend/web/order.html'
                            # 发送信息到主窗口
                            if self.getNewOrders():
                                self.MainWin.Notification.emit(URL,1)
                            else:
                                self.MainWin.Notification.emit(URL,0)
                        is_match = core.vendor.requestByURL.matchURL(str(buf))
                        if is_match:  # 请求网页
                            header = {'user-agent': random.choice(computer)}
                            res = requests.get(str(buf), headers=header)
                    except Exception,e:
                        self.s.close()
                        print e
                        pass

            except socket.error, e:
                print "Dialogue Over from recv %s" % e
                break
        # host = 'localhost'
        time.sleep(3)
        host = '114.215.209.164'
        connectServer(host, 1234, self.user,self.MainWin) # 子进程

    '''
       发送信息
    '''
    def sendMessage(self):
        try:
            data = self.user + '\r\n'
            self.s.send(data)
        except socket.error, e:
            print "Dialogue Over %s" % e
            self.s.close()
            # sys.exit(0)
        # 以下代码可实现聊天客户端的发送消息功能
        while 1:
            try:
                timeDelta = time.time() - self.startTime

                if timeDelta >= 600:
                    print timeDelta
                    data = 'test:1' + '\r\n'
                    self.s.send(data)
                    self.startTime = time.time()
                if timeDelta >= 3600:
                    self.s.close()
                    print 'socket close'
                    break
                # data = raw_input('I say:') + '\r\n'
                # self.s.send(data)
            except socket.error, e:
                print "Dialogue Over  from send %s" % e
                break
    '''
        打印订单
    '''
    def getNewOrders(self):
        try:
            if self.user:
                return Printer().printerCtl('http://yii.kuaxiango.com/api/web/v1/notify/new-order',
                                            {'shop': self.user})
        except Exception:
            pass

'''
    连接服务器
'''
def connectServer(host,port,user,MainWin):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.connect((host, port))
        valid = 'orAngeOfhiSpaiNtHatCanNOTgObaCk' + '\r\n'
        s.send(valid)
    except socket.error, e:
        print "Address-related error connecting to server: %s" % e
        time.sleep(3)
        connectServer(host, port, user,MainWin)
    thPool = []
    for i in range(2):
        thPool.append(socketThread(i,s,user,MainWin))
    for th in thPool:
        th.start()
    for th in thPool:
        th.join()


if __name__ == '__main__':
    # host = '114.215.209.164'
    host = 'localhost'
    port = 1234
    connectServer(host, port, 'test')
