# -*- coding: utf-8 -*-
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.migrate import *
import datetime
import random
from hashlib import sha1

db = SqliteExtDatabase('./data/test.db')

def get_hexdigest(salt, raw_password):
    data = salt + raw_password
    return sha1(data.encode('utf8')).hexdigest()

@db.func()   # fn.make_password
def make_password(raw_password):
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)

@db.func()   # fn.check_password
def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    return hsh == get_hexdigest(salt, raw_password)

class BaseModel(Model):
    class Meta:
        database = db

# 用户信息表
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    secret_key = CharField(null = True)
    add_time = DateTimeField(default=datetime.datetime.now)


# 联系人
class Contact(BaseModel):
    user = CharField(default='qq_qun')
    qq = IntegerField(unique=True)
    qun_name = CharField(default='')
    role = IntegerField(default=0)
    has_weixin = BooleanField(default=True)
    is_added = BooleanField(default=False)
    add_time = DateTimeField(default=datetime.datetime.now)
    devices = CharField(default='andrid phone')
    added_time = DateTimeField(default=datetime.date(2016, 11, 30))

# 设置表单
class Setting(BaseModel):
    per_day = IntegerField(default=20)
    per_add = IntegerField(default=5)
    sleep_time = IntegerField(default=5)
    next_exec = IntegerField(default=3600)
    is_auto = BooleanField(default=False)


if __name__ == '__main__':
    try:
        User.create_table()  # 创建表
    except OperationalError:
        print "User table already exists!"

    try:
        Contact.create_table()
    except OperationalError:
        print "Contact table already exists!"

    try:
        Setting.create_table()
    except OperationalError:
        print "Setting table already exists!"

    # 增加字段代码
    migrator = SqliteMigrator(db)

    # devices = CharField(default='andrid phone')
    # added_time = DateTimeField(default=datetime.date(2016,11,30))
    is_auto = BooleanField(default=False)

    with db.transaction():
        migrate(
            # migrator.add_column('Contact', 'devices', devices),
            # migrator.add_column('Contact', 'added_time', added_time),
            # migrator.drop_column('Contact', 'added_time'),
            migrator.add_column('Setting', 'is_auto', is_auto),
        )