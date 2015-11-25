__author__ = 'johnnytsai'
import settings

def baseUrl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'ROOT_URL': scheme + request.get_host(), }

def baseUrl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'BASE_URL_BACKEND': scheme + request.get_host() + '/backend', }


def staticUrl(request):

    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'STATIC_URL': scheme + request.get_host() + settings.STATIC_URL, }
