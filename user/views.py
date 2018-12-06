from django.http import HttpResponse
from django.shortcuts import render,redirect
from view.views import *
from user.models import *
from utils.commonutils import *
from django import forms

# Create your views here.

# ————————注册————————————
class RegisterView(BaseView):
    template_name = 'register.html'

class RegisterControlView(BaseRedirectView):
    redirect_url = '/user/usercenter/'
    def handle(self,request,*args,**kwargs):
        try:
            user = User.register(**request.POST.dict())
            request.session['user'] = user
        # ————存在问题 ————
        except User.UserExistException as e:
            print(e.args)
        # ————存在问题 ————  解决方法，利用中间件判断user不存在直接在请求之间重定向走

# ———————用户中心———————————
class UserCenterView(BaseView):
    template_name = 'user.html'

# ————————登录————————————
class LoginView(BaseView):
    template_name = 'login.html'

class LoginControl(BaseRedirectView):
    redirect_url = '/user/usercenter/'
    def handle(self,request,*args,**kwargs):
        try:
            user = User.login(**request.POST.dict())
            request.session['user'] = user
        except User.UserNotFoundException as e:
            print(e.args)
            # return render(request,'login.html',{'error':'用户不存在'}) 利用中间件完美解决这个问题

# ————————地址管理————————————
# 处理POST请求需要清理数据
class AddressForm(forms.Form):
    provinceid = forms.IntegerField(required=False)
    cityid = forms.IntegerField(required=False)
    areaid = forms.IntegerField(required=False)
    details = forms.CharField(required=False)
    name = forms.CharField(required=False)
    phone = forms.CharField(required=False)

class AddressView(BaseView,OperateView):
    template_name = 'address.html'
    form_cls = AddressForm
    # 处理GET请求
    def get_extra_context(self, request):
        default_citys = get_citys_by_id(provinces[0]['id'])
        default_areas = get_areas_by_id(default_citys[0]['id'])
        user = request.session['user']
        address = user.address_set.all()
        return {'provinces':provinces,'citys':default_citys,'areas':default_areas,'address':address}
    # 处理POST请求
    def get_province(self,request,provinceid,*args,**kwargs):
        data = []
        citys = get_citys_by_id(str(provinceid))
        data.append(citys)
        data.append(get_areas_by_id(citys[0]['id']))
        return data
    def get_citys(self,request,cityid,*args,**kwargs):
        return get_areas_by_id(str(cityid))
    # POST请求中处理保存地址
    def save_address(self,request,name,phone,provinceid,areaid,cityid,details):
        user = request.session['user']
        province = get_province_by_id(provinceid)
        city = get_city_by_id(provinceid,cityid)
        area = get_area_by_id(cityid,areaid)
        try:
            address = Address.objects.create(name=name,phone=phone,province=province,city=city,area=area,details=details,user=user)
            return {'errorcode':200,'errormsg':''}
        except:
            return {'errorcode':-300,'errormsg':'添加失败'}