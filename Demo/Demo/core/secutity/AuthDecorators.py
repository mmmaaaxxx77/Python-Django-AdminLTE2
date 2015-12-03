from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

__author__ = 'johnnytsai'


def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


def ajax_permission_required(codename2):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated():
                raise PermissionDenied
            if not request.user.has_perm(codename2):
                return JsonResponse(dict(success=False, result="Permission denied"))
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
