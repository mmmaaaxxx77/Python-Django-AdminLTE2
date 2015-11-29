# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
__author__ = 'johnnytsai'


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


