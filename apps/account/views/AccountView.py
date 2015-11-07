# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import json
from Demo.core.secutity.authDecorators import ajax_login_required

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'account/index.html', {'users': User.objects.all()})


@ajax_login_required
def getUsers(request):

    page = request.GET['page']
    limit = 10 if request.GET['limit'] else request.GET['limit']

    users = serializers.serialize('json', User.objects.all(), fields=('username', 'last_login', 'email', 'date_joined'))
    users = json.loads(users)
    return JsonResponse(dict(users=users))


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
