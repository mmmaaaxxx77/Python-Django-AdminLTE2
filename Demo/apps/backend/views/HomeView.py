# -*- coding: utf-8 -*-

import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from apps.backend.models import User
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from Demo import settings
from Demo.context_processors import baseUrl

__author__ = 'johnnytsai'


@login_required
def index(request):
    if request.method == 'GET':
        # user = User(name='johnny')
        return render(request, 'backend/index.html', {})

def getMenuJS(request):
    dic = baseUrl(request)
    return HttpResponse(render_to_string("backend/layout/menuData.html", dic), content_type="text/javascript; charset=UTF-8")

def test_json(request):
    if request.method == 'GET':
        return JsonResponse(dict(foo='bar'))
