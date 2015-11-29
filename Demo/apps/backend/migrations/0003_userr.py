# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('createDate', models.DateTimeField()),
                ('updateDate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
