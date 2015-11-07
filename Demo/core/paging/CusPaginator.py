from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import json
from django.core import serializers
from django.http import JsonResponse

__author__ = 'johnnytsai'


def getUpPagingJSONResult(object, page, size, fields):
    objects = object.objects.all()
    paginator = Paginator(objects, size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
        page = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    objects = serializers.serialize('json', objects ,fields=fields)
    objects = json.loads(objects)

    return JsonResponse(dict(success=True, result=objects, page=page, totalPages=paginator.num_pages, totalResults=paginator.count))
