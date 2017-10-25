# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-30 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20170630_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='Join_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('post_article', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.People_Article')),
                ('post_photo', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.People_Photo_Post')),
                ('post_trips', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.People_Trips')),
            ],
        ),
    ]
