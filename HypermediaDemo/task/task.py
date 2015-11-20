from django.contrib.auth.models import User

__author__ = 'johnnytsai'

def hello():
    print("hello")
    print(User.objects.all())

