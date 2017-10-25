# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-24 12:47
from __future__ import unicode_literals

from django.db import migrations
import geosimple.fields


class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='states',
            name='location',
            field=geosimple.fields.GeohashField(db_index=True, default=(50.822482, -0.141449), max_length=12),
            preserve_default=False,
        ),
    ]