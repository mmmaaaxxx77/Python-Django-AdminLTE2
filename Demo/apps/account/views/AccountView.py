# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
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
import mimetypes
from os.path import basename

__author__ = 'johnnytsai'
mimetypes.init()

@login_required
def index(request):
    return render(request, 'account/index.html', {'loginUser': request.user, 'users': User.objects.all()})


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
    obj = setUpPagingObject(UserProfile, page, size,
                                 filter=None if 'username' not in request.GET else {
                                     'username': request.GET['username']},
                                 sort=None if 'sort' not in request.GET else request.GET['sort'])
    data = UserProfileSerializer(instance=obj['result'], many=True).data
    return generatePagingJSONResult(obj, data)

@ajax_login_required
def getUser(request, username):
    u = User.objects.get(username=username)
    up = UserProfile.objects.get(user=u)
    return JsonResponse(UserProfileSerializer(instance=up, many=False).data)

@ajax_login_required
def getUserProfiles(request):
    #objects = UserProfileSerializer(instance=UserProfile.objects.filter(user__username="test"), many=True).data
    objects = UserProfileSerializer(instance=UserProfile.objects.all(), many=True).data
    return JsonResponse(dict(result=objects))

@ajax_login_required
def newUser(request):

    # 新增使用者 username, password
    if request.method == 'POST':
        data = request.POST.dict()
        #u = User(**data)
        u = None
        try:
            u = User.objects.create(**data)
        except IntegrityError:
            return JsonResponse(dict(success=False, result="使用者名稱重覆"))
        if u == None:
            return JsonResponse(dict(success=False, result="使用者新增失敗"))
        up = UserProfile()
        up.user = u
        if 'file' in request.FILES:
            up.profile_image = request.FILES['file']
        up.save()
        return JsonResponse(dict(success=True, result=UserProfileSerializer(instance=up, many=False).data))


@ajax_login_required
def deleteUser(request, username):
    # 刪除使用者
    if request.method == 'POST':
        #username = username
        try:
            u = User.objects.get(username=username)
            UserProfile.objects.get(user=u).delete()
            u.delete()
            return JsonResponse(dict(success=True, result=None))
        except:
            return JsonResponse(dict(success=False, result="刪除"+username+"失敗"))
    else:
        return JsonResponse(dict(success=False))


@ajax_login_required
def getPermissions(request):
    permissions = serializers.serialize('json', Permission.objects.all())
    permissions = json.loads(permissions)
    return JsonResponse(dict(permissions=permissions))


def getProfileImage(request):
    path = request.GET['path']
    f = open(path, "rb")
    mime_type_guess = mimetypes.guess_type(basename(f.name))
    return HttpResponse(f, content_type=mime_type_guess[0])

def whoAmI(request):
    u = User.objects.get(username=request.user.username)
    up = UserProfile.objects.get(user=u)
    return JsonResponse(UserProfileSerializer(instance=up, many=False).data)