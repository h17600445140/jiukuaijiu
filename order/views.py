# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from utils.cartutils import SessionCartManager
from utils.alipay import AliPay
from jiukuaijiu.settings import BASE_DIR
from view.views import *
import os
# Create your views here.

# 产生一个支付宝对象
alipay = AliPay(
    appid='2016092300580836',
    app_private_key_path=os.path.join(BASE_DIR, 'keys/app_private_2048'),
    alipay_public_key_path=os.path.join(BASE_DIR, 'keys/alipay_public_2048'),
    return_url='http://127.0.0.1:8000/order/alipay/',
    app_notify_url='http://www.pythoncloude.pythonanywhere.com/alipay/post'
)

class OrderView(View):
    def post(self,request):
        if request.session.get('user'):
            # 用户已经登录，到订单界面
            # 拿到前台发送过来的购物项（订单）
            cartitems = request.POST.get('cartitems')
            request.session['cartitems']=cartitems
            # HttpResponse返回的数据由ajax中的success处理重定向
            return HttpResponse('/order/orderlist/')
        else:
            # 用户没有登录，登录界面
            return HttpResponse('/user/login/')


class OrderListView(BaseView):
    template_name = 'order.html'

    def get_extra_context(self, request):
        # cartitems为'xx,xx,xx:xx,xx,xx:'
        rawcartitems = request.session.get('cartitems',"")
        # del request.session['cartitems'] 这里不需要删除，创建完成订单再删除
        cartitems=rawcartitems.split(":")
        cart_manager = SessionCartManager(request.session)
        order_items=[]
        for cartitem in cartitems:
            # 根据商品, 颜色，尺寸，数量获得订单项
           order_items.append(cart_manager.get_cart_item1(*cartitem.split(',')))
        # 通过存入的user获得address
        user = request.session.get('user')
        address = user.address_set.first()
        allprice = 0
        for order_item in order_items:
            allprice+=order_item.all_price()
        return {'address':address,'orderitems':order_items,'allpirce':allprice,'raworderitems':rawcartitems}

from order.models import *
from goods.models import *
import time
import uuid
class OrderCreatedView(BaseRedirectView):
    redirect_url = '' #要支付的的url

    def handle(self,request):
        print('进来了')
        print(request.GET.get('name'))
        print(request.GET.get('address'))
        print(request.GET.get('phone'))
        print(request.GET.get('type'))
        request.session.modified=True
        # 1/删除购物车记录 orderitems
        del request.session['cartitems']
        orderitems = request.GET.get('orderitems')
        orderitems = orderitems.split(":")
        # ——————————得到总价——————————
        cart_manager = SessionCartManager(request.session)
        price = 0
        for orderitem in orderitems:
            # 千万别使用浏览器传送过来的数据，容易被篡改
            price += cart_manager.get_cart_item1(*orderitem.split(',')).all_price()
        # ————————————————————————
        for orderitem in orderitems:
            # 删除失败
            cart_manager.delete_cart_item(*orderitem.split(','))
        # 2/创建order订单对象，（收货地址，订单项）（未付款，已付款，待发货，待收货，待评价，退货中，退货完成）
        order = Order.objects.create(name=request.GET.get('name'),
                             phone= request.GET.get('phone'),
                             address = request.GET.get('address'),
                             payway = request.GET.get('type'),
                             orderitems=orderitems,
                             user = request.session.get('user'),
                             sign = ''.join(str(uuid.uuid4()).split('-')), # 基本上不会重复（订单的唯一标示）
                             order= str(time.time()*1000)  # 很多可能会重复（标示一个人在什么时间买的东西）
                             )
        # 3/库存--
        for orderitem in orderitems:
            goodsid,colorid,sizeid,count=orderitem.split(',')
            store = Goods.objects.get(id=goodsid).store_set.filter(color_id=colorid).filter(size=Size.objects.get(id = sizeid)).first()
            store.count -=int(count) #库存数量减一,库存减少可以做判断到数量为1
            store.save() # 保存到数据库
        # 4/根据支付方式，生成字符界面
        param = alipay.direct_pay(out_trade_no=order.sign, subject='九块九商城支付', total_amount=str(price))
        url = 'https://openapi.alipaydev.com/gateway.do?'+param
        order.save()  # 未支付状态
        self.redirect_url = url

class AliPayView(View):
    def get(self,request):
        data = request.GET.dict()
        # print(data['out_trade_no'],data['trade_no'],data['total_amount'])
        # 弹出sign字段
        sign = data.pop('sign')
        # 验证
        if alipay.verify(data,sign):
            # 取出订单对象，修改订单状态，添加trade_no(退款)（服务器和支付宝的一个交易凭证）
            order = Order.objects.get(sign = data['out_trade_no'])
            order.status='待发货'
            order.trade_no=data['trade_no']
            order.save()
            # 支付成功界面（让用户选择是否支付成功，跳到订单界面）
            # 重定向到订单界面
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')