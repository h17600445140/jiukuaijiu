#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.urls import path
from order import views
urlpatterns=[
    path('',views.OrderView.as_view()),
    path('orderlist/',views.OrderListView.as_view()),
    path('created/', views.OrderCreatedView.as_view()),
    path('alipay/', views.AliPayView.as_view()),
]