# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-02 23:17
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0053_auto_20170802_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='join_table',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
        ),
    ]
