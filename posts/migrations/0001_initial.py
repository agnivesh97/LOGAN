# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('peopleid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='People_Answer',
            fields=[
                ('answerid', models.AutoField(primary_key=True, serialize=False)),
                ('answertext', models.CharField(max_length=5000)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='People_Answer_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerstatus', models.CharField(blank=True, max_length=50, null=True)),
                ('answerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Answer')),
            ],
        ),
        migrations.CreateModel(
            name='People_Article',
            fields=[
                ('articleid', models.AutoField(primary_key=True, serialize=False)),
                ('articletext', models.CharField(max_length=5000)),
                ('ratings', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='People_Article_Comment',
            fields=[
                ('commentid', models.AutoField(primary_key=True, serialize=False)),
                ('commenttext', models.CharField(blank=True, max_length=5000)),
                ('articlecommentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Article')),
            ],
        ),
        migrations.CreateModel(
            name='People_Article_Comment_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=50)),
                ('articlecommentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Article_Comment')),
                ('articleid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Article')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='People_Article_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=50)),
                ('articleid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Article')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='People_Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followid', to='posts.People')),
                ('followingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followingid', to='posts.People')),
            ],
        ),
        migrations.CreateModel(
            name='People_Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(blank=True, max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='People_Question',
            fields=[
                ('quesid', models.AutoField(primary_key=True, serialize=False)),
                ('questiontext', models.CharField(max_length=5000)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='People_Question_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('photoid', models.AutoField(primary_key=True, serialize=False)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('rating', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('place_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(default='Enter trek type, e.g. Himalyan Trek, Western Ghats Trek etc', max_length=200)),
                ('region', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('Cover_Pic', models.FileField(blank=True, null=True, upload_to='')),
                ('about_the_trek', models.TextField(default='Let us know if you have been here..')),
                ('highest_altitude', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('state', models.CharField(default='Let us know if you have been here..', max_length=50)),
                ('wildlife_reserve', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('best_time', models.TextField(default='Let us know if you have been here..')),
                ('exploration_spots', models.TextField(default='Let us know if you have been here..')),
                ('hardness', models.TextField(default='Let us know if you have been here..')),
                ('trail_highlights', models.TextField(default='Let us know if you have been here..')),
                ('trek_duration', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('trek_length', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('endurance_level', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('difficulty', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('route_to_base_camp', models.CharField(default='Let us know if you have been here..', max_length=120)),
                ('route_details', models.TextField(default='Let us know if you have been here..')),
                ('base_village', models.CharField(default='Enter Base Vilage Here..', max_length=120)),
                ('summit_point', models.CharField(default='Enter Base Vilage Here..', max_length=120)),
                ('trek_route', models.TextField(default='Let us know if you have been here..')),
                ('food_tips', models.TextField(default='Let us know if you have been here..')),
                ('water_tips', models.TextField(default='Let us know if you have been here..')),
                ('stay_tips', models.TextField(default='Let us know if you have been here..')),
                ('equipments_tips', models.TextField(default='Let us know if you have been here..')),
                ('fitness_tips', models.TextField(default='Let us know if you have been here..')),
                ('permissions', models.TextField(default='Let us know if you have been here..')),
                ('accomodation', models.TextField(default='Let us know if you have been here..')),
                ('police_station', models.CharField(default='Let us know if you have been here..', max_length=200)),
                ('railway_station', models.CharField(default='Let us know if you have been here..', max_length=200)),
                ('airport', models.CharField(default='Let us know if you have been here..', max_length=200)),
                ('hospital', models.TextField(default='Let us know if you have been here..')),
                ('atm', models.TextField(default='Let us know if you have been here..')),
                ('bus_stand', models.CharField(default='Let us know if you have been here..', max_length=200)),
                ('petrol_pump', models.TextField(default='Let us know if you have been here..')),
                ('mobile_signals', models.TextField(default='Let us know if you have been here..')),
                ('service_station', models.TextField(default='Let us know if you have been here..')),
                ('local_govt_authority', models.TextField(default='Let us know if you have been here..')),
                ('Summit_Coordinates', models.CharField(blank=True, default='null', max_length=120, null=True)),
                ('Base_Village1_Coordinates', models.CharField(blank=True, default='null', max_length=120, null=True)),
                ('Base_Village2_Coordinates', models.CharField(blank=True, default='null', max_length=120, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place_Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
                ('place_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('videoid', models.AutoField(primary_key=True, serialize=False)),
                ('video', models.URLField(blank=True, null=True)),
                ('rating', models.FloatField()),
                ('placeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People')),
            ],
        ),
        migrations.AddField(
            model_name='photos',
            name='placeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='photos',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_question_status',
            name='placeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_question_status',
            name='quesid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Question'),
        ),
        migrations.AddField(
            model_name='people_question_status',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_question',
            name='place_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_question',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_place',
            name='place_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_place',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_article_comment',
            name='photoid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Photos'),
        ),
        migrations.AddField(
            model_name='people_article_comment',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_article',
            name='photoid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Photos'),
        ),
        migrations.AddField(
            model_name='people_article',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_answer_status',
            name='placeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_answer_status',
            name='questionid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Question'),
        ),
        migrations.AddField(
            model_name='people_answer_status',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
        migrations.AddField(
            model_name='people_answer',
            name='answerquesid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People_Question'),
        ),
        migrations.AddField(
            model_name='people_answer',
            name='placeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Place'),
        ),
        migrations.AddField(
            model_name='people_answer',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.People'),
        ),
    ]
