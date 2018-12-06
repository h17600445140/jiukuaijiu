#coding=UTF-8
from  django.core.paginator import  Paginator

class MuitlObjectReturned():

    per_page = 8
    objects = None
    objects_name = 'objects'

    def get_objects(self,page_num = '1'):
        paginator = Paginator(self.objects,self.per_page)
        page_num = int(page_num)
        if page_num < 1 :
            page_num = 1
        if page_num > paginator.num_pages :
            page_num = paginator.num_pages
        page = paginator.page(page_num)
        return {'page':page,'page_range':paginator.page_range,self.objects_name:page.object_list}
