# -*- coding: utf-8 -*-

from baseModel import *
from commands import *

class setting(Setting):
    def __init__(self):
        Setting.__init__(self)

    # 插入新的信息
    def insertVal(self, **kwargs):
        # 过滤重复数据报错
        try:
            self.per_day = kwargs['per_day']
            self.per_add = kwargs['per_add']
            self.sleep_time = kwargs['sleep_time']
            self.next_exec = kwargs['next_exec']
            self.is_auto = kwargs['is_auto']
            self.save()
        except:
            pass

    # 微信记录更新记录
    def updateSetting(self,**kwargs):
        query = Setting.update(per_day=kwargs['per_day'],
                               per_add = kwargs['per_add'],
                               sleep_time=kwargs['sleep_time'],
                               next_exec=kwargs['next_exec'],
                               is_auto=kwargs['is_auto']).where(Setting.id == 1)
        return query.execute()

    # 获取设置记录
    def getSetting(self):
        query = Setting.select()
        return [[item.per_day, item.per_add, item.sleep_time,item.next_exec,item.is_auto] for item in query]




if __name__ == '__main__':
    a = setting().getSetting()
    print a
    setting().save()
    print setting.id