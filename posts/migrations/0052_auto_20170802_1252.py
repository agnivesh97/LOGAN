# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-02 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0051_auto_20170802_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='photo',
            field=models.URLField(default='https://www.google.co.in/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwjxp8L2yrjVAhWDW5QKHWwNDKYQjRwIBw&url=http%3A%2F%2Fwww.mankiyatra.com%2Fusertestimonial&psig=AFQjCNHFNoS_VTV7qfbKqX6A6x8_JshGng&ust=1501764516880556'),
        ),
    ]
