# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-03 09:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0055_remove_join_table_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('place_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reu_place', to='posts.Place')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reu_people', to='posts.People')),
            ],
        ),
    ]
