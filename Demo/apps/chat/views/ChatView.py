# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'chat/index.html', {'users': User.objects.all()})


