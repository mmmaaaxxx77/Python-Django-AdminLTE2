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

accountUrl = [  # Account
                url(r'^$', 'apps.account.views.AccountView.index', name='account_index'),
                url(r'^urls.js$', 'apps.account.views.AccountView.getUrls', name='account_urls'),
                url(r'^data/$', 'apps.account.views.AccountView.dataJS', name='test'),
                url(r'^users/$', 'apps.account.views.AccountView.getUsers', name='account_getUsers'),
                url(r'^users/(?P<username>\w+)/$', 'apps.account.views.AccountView.getUser', name='account_getUser'),
                url(r'^user/$', 'apps.account.views.AccountView.newUser', name='account_newUser'),
                url(r'^user/delete/(?P<username>\w+)/$', 'apps.account.views.AccountView.deleteUser', name='account_deleteUser'),
                url(r'^userP/$', 'apps.account.views.AccountView.getUserProfiles', name='account_getUserPs'),
                url(r'^profileImage/$', 'apps.account.views.AccountView.getProfileImage', name='account_getProfileImage'),
                url(r'^whoAmI/$', 'apps.account.views.AccountView.whoAmI', name='account_whoAmI'),]

permissionUrl = [  # permission
    url(r'^permission/$', 'apps.account.views.PermissionView.index', name='permission_index'),
    url(r'^permission/urls.js$', 'apps.account.views.PermissionView.getUrls', name='permission_urls'),
    url(r'^permissions/$', 'apps.account.views.PermissionView.getPermissions', name='permission_getPermissions'),]

urlpatterns = accountUrl + permissionUrl + [
    # Group
    url(r'^group/$', 'apps.account.views.GroupView.index'), ]
