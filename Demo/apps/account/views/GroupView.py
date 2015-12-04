# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User, Permission
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from Demo.core.paging.CusPaginator import setUpPagingObject, generatePagingJSONResult, setUpPagingObjects
from Demo.core.secutity.AuthDecorators import ajax_login_required, ajax_permission_required
from Demo.core.url.urlUtil import getAllFullUrl
from apps.account.serializers.GroupSerializer import GroupSerializer
from apps.account.serializers.UserSerializer import UserSerializer
import apps.account.urls as _url

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'group/index.html',)


@ajax_login_required
def getUrls(request):
    urls = getAllFullUrl(request, _url.globalUrl + _url.groupUrl, "account")
    return HttpResponse(render_to_string("backend/layout/urls.html", dict(urls=urls)), content_type="text/javascript; charset=UTF-8")


@ajax_login_required
def getGroups(request):
    page = 1 if 'page' not in request.GET else request.GET['page']
    size = 10 if 'size' not in request.GET else request.GET['size']
    obj = setUpPagingObject(Group, page, size,
                                 filter=None if 'name' not in request.GET else {
                                     'name': request.GET['name']},
                                 sort=None if 'sort' not in request.GET else request.GET['sort'])
    data = GroupSerializer(instance=obj['result'], many=True).data
    return generatePagingJSONResult(obj, data)


@ajax_login_required
def getGroupUsers(request, name):
    page = 1 if 'page' not in request.GET else request.GET['page']
    size = 10 if 'size' not in request.GET else request.GET['size']
    group = Group.objects.get(name=name)
    users = User.objects.filter(Q(groups=group))
    obj = setUpPagingObjects(users, page, size)
    data = UserSerializer(instance=obj['result'], many=True).data
    return generatePagingJSONResult(obj, data)


@ajax_login_required
def getGroup(request, name):
    group = Group.objects.get(name=name)
    return JsonResponse(dict(success=True, result=GroupSerializer(instance=group, many=False).data))

@ajax_login_required
def newGroup(request):

    # 新增Group name
    if request.method == 'POST':
        data = request.POST.dict()
        u = None
        try:
            u = Group.objects.create(**data)
        except IntegrityError:
            return JsonResponse(dict(success=False, result="name already exist"))

        return JsonResponse(dict(success=True, result=GroupSerializer(instance=u, many=False).data))


def deleteGroup(request, name):
    if request.method == 'POST':
        try:
            Group.objects.get(name=name).delete()
            return JsonResponse(dict(success=True, result=""))
        except:
            return JsonResponse(dict(success=False, result="delete group fail"))


@ajax_permission_required(codename2='change_user')
def deleteUserGroup(request, username, name):
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=name)
        user.groups.remove(group)
        return JsonResponse(dict(success=True, result=""))
    except:
        return JsonResponse(dict(success=False, result="remove user group fail"))


@ajax_permission_required(codename2='change_group')
def editGeoup(request, name):
    if request.method == 'POST':
        new_permissions = [] if 'permissions' not in request.POST else request.POST.getlist('permissions')

        permissions = []
        for p in new_permissions:
            o = Permission.objects.get(codename=p)
            permissions.append(o)

        u = Group.objects.get(name=name)
        u.permissions.clear()
        u.permissions.add(*permissions)

        return JsonResponse(dict(success=True, result=""))

