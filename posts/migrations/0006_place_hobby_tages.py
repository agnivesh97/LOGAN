# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-25 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0005_auto_20170624_2000'),
        ('posts', '0005_place_t'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='hobby_tages',
            field=models.ManyToManyField(default='', to='search_app.hobbytag'),
        ),
    ]