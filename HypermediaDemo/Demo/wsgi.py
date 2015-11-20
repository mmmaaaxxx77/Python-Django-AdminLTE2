"""
WSGI config for Demo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from task.task import hello
from task.threadtest import run

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Demo.settings")

application = get_wsgi_application()

hello()
run()