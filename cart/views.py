from django.shortcuts import render

# Create your views here.
from view.views import *
from utils.cartutils import *
from django import forms

class MyForm(forms.Form):
    goodsid = forms.IntegerField()
    colorid = forms.IntegerField()
    sizeid  = forms.IntegerField()
    count = forms.IntegerField(required=False)
    # def clean(self):
    #     super(MyForm,self).clean()
    #     data = self.cleaned_data
    #     count = data['count']
    #     if count<0:
    #         self.errors['count']=['商品数量不能小于0']

#CartView完成的功能:添加购物项，重定向到购物车界面
class CartView(BaseRedirectView):
    redirect_url = '/cart/cart.html'
    def handle(self,request,*args,**kwargs):
        # 处理业务逻辑
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        cart_manager.add_cart_item(**request.POST.dict())

#显示购物车界面
class CartListView(BaseView,OperateView):
    template_name = 'cart.html'
    form_cls = MyForm
    # 处理GET
    def get_extra_context(self, request):
        cart_manager = SessionCartManager(request.session)
        return {'cartItems':cart_manager.get_all_cart_items()}

    #处理POST
    def add(self,request,goodsid,colorid,sizeid,*args,**kwargs):
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        #写的代码没有绝对正确的
        try:
            cart_manager.add_cart_item(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=1)
            #大前端（android/ios/前端）{'ok'}  {"errorcode":-100,'errormsg':e.message} 接受json数据
            return {"errorcode": 200, 'errormsg': ""}
        except Exception as e:
            return {"errorcode": -100, 'errormsg': e.args}

    def min(self,request,goodsid,colorid,sizeid,*args,**kwargs):
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        #写的代码没有绝对正确的
        try:
            cart_manager.add_cart_item(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=-1)
            #大前端（android/ios/前端）{'ok'}  {"errorcode":-100,'errormsg':e.message} 接受json数据
            return {"errorcode": 200, 'errormsg': ""}
        except Exception as e:
            return {"errorcode": -100, 'errormsg': e.args}

    def delete(self,request,goodsid,colorid,sizeid,*args,**kwargs):
        request.session.modified = True
        cart_manager = SessionCartManager(request.session)
        try:
            cart_manager.delete_cart_item(goodsid=goodsid,colorid=colorid,sizeid=sizeid)
            return {"errorcode": 200, 'errormsg': ""}
        except Exception as e:
            return {"errorcode": -100, 'errormsg': "删除失败"}