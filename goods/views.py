from django.shortcuts import render

# Create your views here.
from django.views import View
from goods.models import *
from django.core.paginator import Paginator

from  view.views import BaseView
from  utils.pageutils import MuitlObjectReturned
class GoodsListView(BaseView,MuitlObjectReturned):
    # 所有不变的东西，都放到了类的成员当中
    template_name = 'index.html'
    objects_name = 'goods'
    category_objects = Category.objects.all()

    def prepare(self,request):
        category_id = int(request.GET.get('category_id',Category.objects.first().id))
        self.objects=Category.objects.get(id =category_id ).goods_set.all()
        self.category_id = category_id

    def get_extra_context(self, request):
        page_num = request.GET.get('page',1)
        context = {'category_id':self.category_id,'categorys':self.category_objects}
        context.update(self.get_objects(page_num))
        return  context

class GoodsDetailsView(BaseView):
    template_name = 'details.html'

    def handle_request_cookie(self, request):
        # 获得cookie
        self.historys = eval(request.COOKIES.get('history','[]'))
        self.historys.reverse()

    def handle_response_cookie(self, response):
        # 通过COOKIE设置商品浏览记录
        if self.goodsId not in self.historys:
            self.historys.append(self.goodsId)
        elif self.goodsId in self.historys:
            del self.historys[self.historys.index(self.goodsId)]
            self.historys.append(self.goodsId)
        response.set_cookie('history',str(self.historys),expires=60*60*24*14)

    def get_extra_context(self, request):
        goodsId = int(request.GET.get('goodsId'))
        good = Goods.objects.get(id=goodsId)
        # 处理浏览过的商品
        self.goodsId = goodsId
        recommend_goods=[]
        for id in self.historys:
            recommend_goods.append(Goods.objects.get(id=id))
        return {'good':good,'goods_details':good.goodsdetails_set.all(),'recommend_goods':recommend_goods}
# ——————————————————————————————————

# class BaseView(View):
#     template_name = None
#     context = {}
#
#     def get(self,request,*args,**kwargs):
#         return render(request,self.template_name,self.get_context(request))
#
#     def get_context(self,request):
#         self.context.update(self.get_extra_context(request))
#         return self.context
#
#     def get_extra_context(self, request):
#         pass
#
#
# class MultiObjectReturned(BaseView):
#     model = None
#     objects_name = 'objects'
#
#     def get_objects(self,page_num='1',per_page=12,objects=None,*args,**kwargs):
#         if objects==None:
#             pagintor = Paginator(self.model.objects.all(),per_page)
#         else:
#             pagintor = Paginator(objects,per_page)
#         page_num = int(page_num)
#         if page_num < 1:
#             page_num = 1
#         if page_num > pagintor.num_pages:
#             page_num=pagintor.num_pages
#         page = pagintor.page(page_num)
#         return {'page':page,self.objects_name:page.object_list,'page_range':pagintor.page_range}
#
#
# class GoodsListView(MultiObjectReturned):
#     template_name = 'index.html'
#     objects_name = 'goods'
#
#     def get_extra_context(self, request):
#         category_id = int(request.GET.get('category_id',Category.objects.first().id))
#         self.category_id = category_id
#         page_num = request.GET.get('page',1)
#         self.get_objects(page_num)
#         context={}
#         context['category_id']=category_id
#         context['categorys']=Category.objects.all()
#         return context
#     def get_objects(self,page_num='1',per_page=4,objects=None,*args,**kwargs):
#         objects = Category.objects.get(id=self.category_id).goods_set.all()
#         self.context.update(MultiObjectReturned.get_objects(self, page_num, per_page, objects=objects))
