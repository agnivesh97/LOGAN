# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-25 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0006_hobbytag_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='hobbytag',
            name='extra_tags',
            field=models.ManyToManyField(default='', to='search_app.extra_tag'),
        ),
    ]