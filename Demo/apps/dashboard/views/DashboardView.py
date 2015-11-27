# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import json
from Demo.core.secutity.AuthDecorators import ajax_login_required
from Demo.core.paging.CusPaginator import getUpPagingJSONResult
from django.template.loader import render_to_string

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


