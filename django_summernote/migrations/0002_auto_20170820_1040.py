# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-20 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_summernote', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='name',
            field=models.CharField(blank=True, help_text='Defaults to filename, if left blank', max_length=255, null=True),
        ),
    ]
