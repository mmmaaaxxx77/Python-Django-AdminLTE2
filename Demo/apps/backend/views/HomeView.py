from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from apps.backend.models import User
from django.http import JsonResponse
from Demo import settings

__author__ = 'johnnytsai'


@login_required
def index(request):
    if request.method == 'GET':
        # user = User(name='johnny')
        return render(request, 'backend/index.html', {})


def test_json(request):
    if request.method == 'GET':
        return JsonResponse(dict(foo='bar'))
