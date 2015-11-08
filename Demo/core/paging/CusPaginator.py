from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import json
from django.core import serializers
from django.http import JsonResponse

__author__ = 'johnnytsai'


def getUpPagingJSONResult(object, page, size, **dic):
    # filter
    if 'filter' in dic and dic['filter'] is not None:
        objects = object.objects.filter(**dic['filter'])
    else:
        objects = object.objects.all()

    # sort
    if 'sort' in dic and dic['sort'] is not None:
        objects = objects.extra(order_by=[dic['sort']])

    # paging
    paginator = Paginator(objects, size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
        page = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    # list to json
    objects = serializers.serialize('json', objects, fields=None if 'fields' not in dic else dic['fields'])
    objects = json.loads(objects)

    return JsonResponse(dict(success=True, result=objects, page=page, totalPages=paginator.num_pages, totalResults=paginator.count))
