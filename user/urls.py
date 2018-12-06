#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.urls import path
from user import views
urlpatterns=[
    path('register/',views.RegisterView.as_view()),
    path('registercontrol/',views.RegisterControlView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('logincontrol/',views.LoginControl.as_view()),
    path('usercenter/',views.UserCenterView.as_view()),
    path('address/',views.AddressView.as_view()),
]