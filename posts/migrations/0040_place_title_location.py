# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0039_auto_20170726_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='title_location',
            field=models.CharField(default='', max_length=120),
        ),
    ]
