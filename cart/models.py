from django.db import models

# Create your models here.
from goods.models import *

# 自定义管理器，重写object.all()方法
class CartItemManager(models.Manager):
    def all(self):
        return super(models.Manager,self).all().filter(isdelete=False)

class CartItem(models.Model):
    goodsid = models.IntegerField()
    colorid = models.IntegerField()
    sizeid = models.IntegerField()
    count = models.IntegerField()
    isdelete = models.BooleanField(default=False)
    object = CartItemManager()

    def goods(self):
        return Goods.objects.get(id = self.goodsid)
    def color(self):
        return Color.objects.get(id = self.colorid)
    def size(self):
        return Size.objects.get(id = self.sizeid)
    def all_price(self):
        return self.goods().gprice*(int(self.count))

