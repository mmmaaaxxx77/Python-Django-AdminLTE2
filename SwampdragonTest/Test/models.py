from django.db import models
from swampdragon.models import SelfPublishModel
from Test.serializers import FooSerializer


class Foo(SelfPublishModel, models.Model):
    text = models.CharField(max_length=100)