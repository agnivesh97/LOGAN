# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 10:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170617_0716'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_notification',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('notification', models.CharField(blank=True, max_length=500)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review_place',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('review_text', models.CharField(max_length=5000)),
                ('dateandtime', models.DateField(auto_now=True)),
                ('placeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='Review_place_status',
            fields=[
                ('review_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('helpful', models.BooleanField(default=False, max_length=50)),
                ('report', models.CharField(blank=True, default='none', max_length=20)),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Review_place')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.RemoveField(
            model_name='review',
            name='placeid',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='review_status',
            name='placeid',
        ),
        migrations.RemoveField(
            model_name='review_status',
            name='review_id',
        ),
        migrations.RemoveField(
            model_name='review_status',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Review_status',
        ),
    ]
