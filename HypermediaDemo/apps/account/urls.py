"""Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os

from django.conf.urls import url
from django.contrib.auth.views import login, logout

urlpatterns = [url(r'^$', 'apps.account.views.AccountView.index'),
               url(r'^data/$', 'apps.account.views.AccountView.dataJS'),
               url(r'^users/$', 'apps.account.views.AccountView.getUsers'),
               url(r'^user/$', 'apps.account.views.AccountView.addUser'),
               url(r'^permissions/$', 'apps.account.views.AccountView.getPermissions')]

