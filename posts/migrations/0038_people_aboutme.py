# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-25 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0037_remove_place_places'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='aboutme',
            field=models.CharField(default='Tell somthing about You..', max_length=200),
        ),
    ]