#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.urls import path
from django.conf.urls import re_path
from goods import views

urlpatterns=[
    path('',views.GoodsListView.as_view()),
    re_path(r'goodsdetails/',views.GoodsDetailsView.as_view()),
]