#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016-11-24
@author: xiaocaiyidie
'''
from flask import Flask, session, request, render_template, redirect, url_for,jsonify
import os
# 修复 Pyinstaller 打包程序bug
import six
import appdirs
import SocketServer
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.message import MIMEMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import Encoders
from models.contact import contact
from models.setting import setting

app = Flask(__name__,root_path=os.getcwd()+'/view/app/',)
app.config.update(
    DEBUG=True,
    SECRET_KEY='iLoVeyoUBuTYoUDONtKNowN'
)

@app.route('/',methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/users',methods=['POST', 'GET'])
def user():
    username = request.cookies.get('username')
    if not username:
        username = u'请输入账号'
    islogin = session.get('islogin')
    if islogin:
        return redirect(url_for('user'))
    else:
        return render_template('index.html', username=username)

@app.route('/datas',methods=['POST', 'GET'])
def datas():
    page = request.args.get('num', 1, type=int)
    pageNum = request.args.get('pageNum', 10, type=int)
    qq = contact().allQQ(page,pageNum)
    prevPage = 1 if page==1 else page - 1
    nextPage = 1 if len(qq)<10 else page + 1

    return render_template('datas.html', qq=qq, prevPage=prevPage, nextPage=nextPage)

@app.route('/setting',methods=['POST', 'GET'])
def configs():
    subtype = request.args.get('subtype', 0, type=int)
    settings =setting()
    res = settings.getSetting()

    if len(res) != 0:
        per_day = res[0][0]  # 每天上限
        per_add = res[0][1]  # 每次添加
        sleep_time = res[0][2]  # 添加间息
        next_exec = res[0][3]   # 执行间息
        is_auto = res[0][4]   # 自动执行
    else:
        per_day = 20
        per_add = 5
        sleep_time = 5
        next_exec = 3600
        is_auto = False
    return render_template('setting.html',
                            per_day=per_day,
                            per_add=per_add,
                            sleep_time=sleep_time,
                            next_exec=next_exec,
                            is_auto=is_auto,
                            subtype=subtype)

@app.route('/setting/post',methods=['POST'])
def settingPost():
    settings = setting()
    res = settings.getSetting()
    kwargs = {}
    kwargs['per_day'] = request.form.get('per_day', 20, type=int)
    kwargs['per_add'] = request.form.get('per_add', 5, type=int)
    kwargs['sleep_time'] = request.form.get('sleep_time', 5, type=int)
    kwargs['next_exec'] = request.form.get('next_exec', 3600, type=int)
    kwargs['is_auto'] = request.form.get('is_auto', False, type=int)
    if len(res) == 0:
        settings.insertVal(**kwargs)
    else:
        settings.updateSetting(**kwargs)
    return redirect(url_for('configs',subtype=1))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)