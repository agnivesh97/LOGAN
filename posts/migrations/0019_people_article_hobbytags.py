# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-05 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0008_auto_20170626_1850'),
        ('posts', '0018_auto_20170704_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='people_article',
            name='hobbytags',
            field=models.ManyToManyField(default='', null=True, to='search_app.hobbytag'),
        ),
    ]
