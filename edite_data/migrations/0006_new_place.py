# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-20 04:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0053_auto_20170802_1301'),
        ('edite_data', '0005_place_temp_petrol_pump'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='New_place', to='posts.Place')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='New_people', to='posts.People')),
            ],
        ),
    ]