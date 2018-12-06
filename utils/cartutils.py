#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cart.models import *

class CartManager(object):
    def add_cart_item(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        pass
    def delete_cart_item(self,goodsid,colorid,sizeid,*args,**kwargs):
        pass
    def get_all_cart_item(self,*args,**kwargs):
        pass

class SessionCartManager(CartManager):

    def __init__(self,session):
        self.session = session
    # 从浏览器发送过来的都是字符串

    def add_cart_item(self, goodsid, colorid, sizeid, count,*args,**kwargs):
        # 1、[{"key":CatItem}]  2、[{'key':key,'value':CartItem}] ——两种设计方式
        count = int(count)
        cart = self.session.get('cart',[])
        key = self.__gen_key(goodsid,colorid,sizeid)
        if self.is_exist(cart,key):
            cartitem = self.get_cart_item(cart,key)
            if cartitem.count+count < 1:
                raise Exception()
            cartitem.count += count  #添加商品
            # ————第一种————
            # if cartitem.count < 1:
            #     cartitem.count = 1
            print(cartitem.count)
        else:
            cart.append({key:CartItem(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count)})
        self.session['cart'] = cart

    def delete_cart_item(self, goodsid, colorid, sizeid,*args,**kwargs):
        cart = self.session.get('cart', [])
        key = self.__gen_key(goodsid, colorid, sizeid)
        if self.is_exist(cart,key):
            index = -1
            for i in range(len(cart)):
                keys = list(cart[i].keys())
                if keys[0] == key:
                    index = i
                    break
            if index!=-1:
                del cart[index]

    # 根据购物车获得购物项
    def get_all_cart_items(self,*args,**kwargs):
        cart = self.session.get('cart')
        if cart == None:
            return []
        else:
            cartitems = []
            for cartitem in cart:
                cartitems.extend(cartitem.values())
            return cartitems

    # 根据商品，颜色，尺寸，数量获得订单项
    def get_cart_item1(self,goodsid, colorid, sizeid,*args,**kwargs):
        cart = self.session.get('cart')
        key = self.__gen_key(goodsid, colorid, sizeid)
        if cart == None:
            return None
        else:
            for i in range(len(cart)):
                keys = list(cart[i].keys())
                carts = list(cart[i].values())
                if keys[0] == key:
                    return carts[0]
            # python2
            # for i in range(len(cart)):
            #     if cart[i].keys()[0] == key:
            #         return cart[i].values()[0]

    # 得到购物车里每个商品的key
    def __gen_key(self,goodsid,colorid,sizeid):
        return str(goodsid)+'-'+str(colorid)+'-'+str(sizeid)

    # 得到购物车里每个商品的cartitem
    def get_cart_item(self, cart, key):
        for cartitem in cart:
            keys = list(cartitem.keys())
            if keys[0] == key:
                return cartitem[key]
        return None

    # 判断商品存在还是不存在
    def is_exist(self,cart,key):
        isExist = False
        for cartitem in cart:
            keys = list(cartitem.keys())
            if keys[0] == key:
                isExist = True
                break
        return isExist

# ————————————————————————————————

class UserCartManager(CartManager):
    pass

def get_cart_manager(request):
    if not request.session.get('user',"") :
        return SessionCartManager(request.session)
    else:
        # 值得考虑，需不需要将ssesion中的购物车数据拷贝到数据库
        # 删除session的购物车
        return UserCartManager(request.session)