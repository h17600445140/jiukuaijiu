#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cart import views
from django.urls import path
urlpatterns=[
    path('',views.CartView.as_view()),
    path('cart.html/',views.CartListView.as_view())
]