from django.contrib import auth
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import render

__author__ = 'johnnytsai'


def loginAction(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/backend/')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/backend/')
        else:
            return render(request, 'backend/login.html')
    return render(request, 'backend/login.html')


def logoutAction(request):
    auth.logout(request)
    return render(request, 'backend/login.html')
