# -*- coding: utf-8 -*-


from baseModel import *
from commands import *

class user(User):
    def __init__(self):
        Contact.__init__(self)

    # 插入新的信息
    def insertVal(self, **kwargs):
        # 过滤重复数据报错
        try:
            self.username = kwargs['username']
            self.password = kwargs['password']
            self.secret_key = kwargs['secret_key']
            self.save()
        except:
            pass

    # 获取secrect_key
    def updateKey(self):
        query = Contact.update(has_weixin=0).where(Contact.qq == qq)




if __name__ == '__main__':
    print len(user().getQQ(800))
    print user().noWeixin(332007699)