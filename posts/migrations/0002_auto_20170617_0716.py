# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 07:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='People_Question_Report',
            fields=[
                ('reportid', models.AutoField(primary_key=True, serialize=False)),
                ('reportstatus', models.CharField(max_length=50)),
                ('placeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('review_text', models.CharField(max_length=5000)),
                ('placeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='Review_status',
            fields=[
                ('review_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=25, null=True)),
                ('placeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place')),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Review')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagid', models.AutoField(primary_key=True, serialize=False)),
                ('tagname', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Tag_Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='people_article',
            name='photoid',
        ),
        migrations.RemoveField(
            model_name='people_article_comment',
            name='photoid',
        ),
        migrations.RemoveField(
            model_name='people_question',
            name='time',
        ),
        migrations.AddField(
            model_name='people_answer_status',
            name='answerreport',
            field=models.CharField(blank=True, default='none', max_length=20),
        ),
        migrations.AddField(
            model_name='people_article',
            name='placeid',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_article',
            name='type',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='people_article_comment',
            name='placeid',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_article_status',
            name='placeid',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_article_status',
            name='superstatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='people_question_status',
            name='report',
            field=models.CharField(blank=True, default='none', max_length=20),
        ),
        migrations.AlterField(
            model_name='people_answer_status',
            name='answerstatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='people_article_status',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='people_question_status',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tag_article',
            name='articleid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Article'),
        ),
        migrations.AddField(
            model_name='tag_article',
            name='tagid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Tag'),
        ),
    ]
