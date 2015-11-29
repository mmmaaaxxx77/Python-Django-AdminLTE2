# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151129_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(null=True, upload_to=b'/Users/mmmaaaxxx77/GoogleDrive/PythonProjects/Python-Django-AdminLTE2/Demo/upload/'),
        ),
    ]
