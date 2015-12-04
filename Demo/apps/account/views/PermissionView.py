# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Demo.core.paging.CusPaginator import setUpPagingObject, generatePagingJSONResult, setUpPagingObjects
from Demo.core.secutity.AuthDecorators import ajax_login_required, ajax_permission_required
from Demo.core.url.urlUtil import getAllFullUrl
from apps.account.serializers.UserSerializer import UserSerializer
from apps.account.serializers.PermissionSerializer import PermissionSerializer
import apps.account.urls as _url

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'permission/index.html',)


@ajax_login_required
def getUrls(request):
    urls = getAllFullUrl(request, _url.globalUrl + _url.permissionUrl, "account")
    return HttpResponse(render_to_string("backend/layout/urls.html", dict(urls=urls)), content_type="text/javascript; charset=UTF-8")

@ajax_login_required
def getPermissions(request):
    page = 1 if 'page' not in request.GET else request.GET['page']
    size = 10 if 'size' not in request.GET else request.GET['size']
    obj = setUpPagingObject(Permission, page, size,
                                 filter=None if 'codename' not in request.GET else {
                                     'codename': request.GET['codename']},
                                 sort=None if 'sort' not in request.GET else request.GET['sort'])
    data = PermissionSerializer(instance=obj['result'], many=True).data
    return generatePagingJSONResult(obj, data)


@ajax_login_required
def getPermissionUsers(request, codename):
    page = 1 if 'page' not in request.GET else request.GET['page']
    size = 10 if 'size' not in request.GET else request.GET['size']
    perm = Permission.objects.get(codename=codename)
    #users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm))
    users = User.objects.filter(Q(user_permissions=perm))
    obj = setUpPagingObjects(users, page, size)
    data = UserSerializer(instance=obj['result'], many=True).data
    return generatePagingJSONResult(obj, data)


@ajax_permission_required(codename2='change_user')
def deleteUserPermission(request, username, codename):
    try:
        user = User.objects.get(username=username)
        perm = Permission.objects.get(codename=codename)
        user.user_permissions.remove(perm)
        return JsonResponse(dict(success=True, result=""))
    except:
        return JsonResponse(dict(success=False, result="remove user permission fail"))

