# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-30 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edite_data', '0003_place_temp_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='place_temp',
            name='hospital',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
    ]
