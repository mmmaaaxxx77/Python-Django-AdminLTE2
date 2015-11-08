# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import json
from Demo.core.secutity.AuthDecorators import ajax_login_required
from Demo.core.paging.CusPaginator import getUpPagingJSONResult

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'account/index.html', {'users': User.objects.all()})


@ajax_login_required
def getUsers(request):
    page = 1 if 'page' not in request.GET else request.GET['page']
    size = 10 if 'size' not in request.GET else request.GET['size']
    return getUpPagingJSONResult(User, page, size,
                                 filter=None if 'username' not in request.GET else {
                                     'username': request.GET['username']},
                                 sort=None if 'sort' not in request.GET else request.GET['sort'],
                                 fields=('username', 'last_login', 'email', 'date_joined'))


@ajax_login_required
def addUser(request):
    if request.method == 'POST':
        userdic = json.loads(request.body)
        User.objects.create(**userdic)
        return JsonResponse(dict(success=True))
    return JsonResponse(dict(success=False))
    # return JsonResponse(dict(success=json.loads(request.body)))


@ajax_login_required
def getPermissions(request):
    permissions = serializers.serialize('json', Permission.objects.all())
    permissions = json.loads(permissions)
    return JsonResponse(dict(permissions=permissions))
