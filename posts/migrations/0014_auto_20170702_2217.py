# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-02 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20170702_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people_article_status',
            name='superstatus',
        ),
        migrations.AlterField(
            model_name='people_article_status',
            name='status',
            field=models.CharField(blank=True, default='none', max_length=20),
        ),
    ]