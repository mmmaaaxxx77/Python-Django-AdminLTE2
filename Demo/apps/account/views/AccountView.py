# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import json
from Demo.core.secutity.AuthDecorators import ajax_login_required
from Demo.core.paging.CusPaginator import setUpPagingObject, generatePagingJSONResult
from django.template.loader import render_to_string
from Demo.core.url.urlUtil import getFullUrlFromName, getAllFullUrl
from apps.account.models import UserProfile
from apps.account.serializers.UserProfileSerializer import UserProfileSerializer
from apps.account.serializers.UserSerializer import UserSerializer
import apps.account.urls as _url
from rest_framework import serializers

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'account/index.html', {'users': User.objects.all()})


@ajax_login_required
def getUrls(request):
    urls = getAllFullUrl(request, _url.accountUrl, "account")
    return HttpResponse(render_to_string("backend/layout/urls.html", dict(urls=urls)), content_type="text/javascript; charset=UTF-8")


@ajax_login_required
def dataJS(request):

    print(render_to_string("account/data.html", {'users': User.objects.all()}))
    data = json.loads(render_to_string("account/data.html", {'users': User.objects.all()}))

    # 1
    return HttpResponse(json.dumps(data), content_type="application/javascript")
    # 2
    #return JsonResponse(data)


@ajax_login_required
def getUsers(request):
    page = 1 if 'page' not in request.GET else request.GET['page']
    size = 10 if 'size' not in request.GET else request.GET['size']
    obj = setUpPagingObject(User, page, size,
                                 filter=None if 'username' not in request.GET else {
                                     'username': request.GET['username']},
                                 sort=None if 'sort' not in request.GET else request.GET['sort'])
    data = UserSerializer(instance=obj['result'], many=True).data
    return generatePagingJSONResult(obj, data)


def getUserProfiles(request):
    u = UserProfile.objects.get(user__username="ffff")
    print(u)
    objects = UserProfileSerializer(instance=UserProfile.objects.filter(user__username="ffff"), many=True).data
    return JsonResponse(dict(result=objects))

@ajax_login_required
def editUser(request):

    # 新增使用者 username, password
    if request.method == 'POST':
        data = request.POST.dict()
        u = User(**data)
        u.save()
        up = UserProfile()
        up.user = u
        up.profile_image = data['profile_image']
        up.save()
        return JsonResponse(dict(success=False))
    else:
        return JsonResponse(dict(success=False))


@ajax_login_required
def getPermissions(request):
    permissions = serializers.serialize('json', Permission.objects.all())
    permissions = json.loads(permissions)
    return JsonResponse(dict(permissions=permissions))
