# -*- coding: utf-8 -*-

from baseModel import *
from commands import *

class contact(Contact):
    def __init__(self):
        Contact.__init__(self)

    # 插入新的信息
    def insertVal(self, **kwargs):
        # 过滤重复数据报错
        try:
            self.qq = kwargs['qq']
            self.qun_name = kwargs['qun_name']
            self.role = kwargs['role']
            self.save()
        except:
            pass

    # 微信已经添加
    def weixinAdded(self,qq,devices):
        query = Contact.update(is_added=True,
                               added_time=datetime.datetime.now(),
                               devices=devices).where(Contact.qq== qq)
        return query.execute()

    # 设备当天添加总数
    def deviceAdded(self,devices):
        query = Contact.select().where(Contact.added_time >= datetime.date.today(),
                                       Contact.devices == devices)
        return [[item.qq,item.qun_name,item.is_added,item.devices] for item in query]

    # 微信不存在
    def noWeixin(self,qq):
        query = Contact.update(has_weixin=0).where(Contact.qq== qq)
        return query.execute()

    # 获取QQ
    def getQQ(self,num=5):
        query = Contact.select().order_by(Contact.add_time,'DESC')
        query = query.limit(num).where(Contact.is_added == 0,Contact.has_weixin == 1)
        return [[item.qq,item.qun_name,item.is_added] for item in query]

    # 获取QQ
    def allQQ(self, page=1,pageNum=10):
        query = Contact.select().paginate(int(page), int(pageNum))
        return [[item.qq, item.qun_name, item.is_added] for item in query]

    # test
    # def test(self,qq):
    #     print self.qq
    #     query = Contact.select().where(Contact.qq==qq)
    #     print query
    #     return [[item.qq,item.qun_name] for item in query]



if __name__ == '__main__':
    # print len(contact().getQQ(800))
    print contact().deviceAdded('FA37JS901616')