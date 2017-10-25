# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-29 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edite_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place_temp',
            name='commonly_visited_from',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
        migrations.AddField(
            model_name='place_temp',
            name='duration_of_visit',
            field=models.CharField(default='Let us know if you have been here..', max_length=50),
        ),
        migrations.AddField(
            model_name='place_temp',
            name='govt_guidelines',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
        migrations.AddField(
            model_name='place_temp',
            name='languages_spoken',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
        migrations.AddField(
            model_name='place_temp',
            name='open_timings',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
        migrations.AddField(
            model_name='place_temp',
            name='popular_route',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
        migrations.AddField(
            model_name='place_temp',
            name='weather_details',
            field=models.TextField(default='Let us know if you have been here..'),
        ),
    ]
