from django.db import models
import time
from utils.md5utils import *
# Create your models here.

class User(models.Model):
    account = models.CharField(unique=True,max_length=20)
    password = models.CharField(max_length=64)

    class UserExistException(Exception):
        def __init__(self):
            super(Exception, self).__init__('账号已经存在')

    class UserNotFoundException(Exception):
        def __init__(self):
            Exception.__init__(self,'账号不存在')

    @classmethod
    def register(cls,account,password,*args,**kwargs):
        try:
            user = cls.objects.create(account=account,password=password)
            return user
        except:
            raise cls.UserExistException

    @staticmethod
    def login(account,password,times,*args,**kwargs):
        current_server = time.time()*1000
        if not (int(times) >= current_server-1000*60*10 and int(times) <= current_server):
            return
        try:
            # 先通过账号获得用户
            user = User.objects.get(account=account)
            user_password = md(user.password + times)
            if user_password == password:
                return user
            else:
                return None
        except:
            raise User.UserNotFoundException

class Address(models.Model):
    province = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    area = models.CharField(max_length=10)
    details = models.CharField(max_length=520)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    user = models.ForeignKey(User,models.DO_NOTHING)
    isdelete = models.BooleanField(default=False)
    # 默认收货地址
    isprimary = models.BooleanField(default=False)