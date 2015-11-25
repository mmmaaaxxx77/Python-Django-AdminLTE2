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

urlpatterns = [url(r'^$', 'apps.backend.views.HomeView.index'),
               url(r'^menuJS.js$', 'apps.backend.views.HomeView.getMenuJS'),
               #url(r'^login/$', 'apps.backend.views.SecurityView.loginAction'),
               url(r'^login/$', login, {'template_name':'backend/login.html'}),
               #url(r'^logout/$', 'apps.backend.views.SecurityView.logoutAction'),
               url(r'^logout/$', logout, {'template_name':'backend/login.html'}),
               url(r'^json/$', 'apps.backend.views.HomeView.test_json')]
               #url(r'^image/(?P<path>.*)$', 'django.templates.static.serve',
               #    {'document_root': os.path.join(setting.BASE_DIR, 'apps/backend/web/resources/images')}),

