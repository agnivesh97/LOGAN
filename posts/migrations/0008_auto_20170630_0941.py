# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-30 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_people_photo_post_people_photo_post_comment_people_photo_post_status_people_trips_people_trips_comme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people_photo_post',
            name='photos',
            field=models.ManyToManyField(to='posts.Photos'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='rating',
            field=models.FloatField(default='1'),
        ),
    ]