from django.core import serializers
from django.db import models
import os
from django.db.models import ImageField
from django.contrib.auth.models import User


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    profile_image = ImageField(upload_to="/Users/mmmaaaxxx77/GoogleDrive/PythonProjects/Python-Django-AdminLTE2/Demo/upload/", blank=True, null=True)

    def extra_user(self):
        return serializers.serialize('user', self.user.all())

