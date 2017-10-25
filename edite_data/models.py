from django.db import models
import posts
from posts.models import *
from django.contrib.postgres.fields import JSONField
class Place_temp(models.Model):
    place_id=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='tem_place')
    title = models.CharField(null=True,max_length=120,default='null')
    user_id=models.ForeignKey(People,on_delete=models.CASCADE,related_name='temp_people')
    category = models.CharField(max_length=200, default='')
    region = models.CharField(max_length=120, default='')
    
    #Post_List_img = models.FileField(null=True, blank=True)
    Cover_Pic = models.FileField(null=True, blank=True)
    #Content_Pic = models.ForeignKey(Photos)
    Video_Link = models.CharField(null=True, blank=True, max_length=400, default='')
    state= models.CharField(max_length=50, default='Let us know if you have been here..')
    trail_highlights = models.TextField(null=True ,default='')
    highest_altitude = models.CharField( null=True, max_length=120, default='')
    about_the_trek = models.TextField(null=True, default='')
    access_time = models.TextField(null=True, default='')
    best_time = models.TextField(null=True ,default='')
    Exploration_Spots = models.TextField(null=True, default='')

    trek_duration = models.CharField(null=True, max_length=120, default='')
    trek_length = models.CharField(null=True, max_length=120, default='')
    endurance_level = models.CharField(null=True, max_length=120, default='')
    difficulty = models.CharField(null=True, max_length=120, default='')

    route_to_base_camp = models.CharField(null=True, max_length=120, default='')
    route_details = models.TextField(null=True, default='')
    base_village = models.CharField(null=True, max_length=120, default='')
    trek_route = models.TextField(null=True, default='')
    wildlife_reserve = models.CharField(null=True, max_length=120, default='')
    food_availability = models.TextField(null=True, default='')
    water_availability = models.TextField(null=True, default='')
    shade_availability = models.TextField(null=True, default='')
    accomodation = models.TextField(null=True, default='')

    police_station = models.CharField(null=True, max_length=200, default='')
    atm = models.CharField(null=True,max_length=200, default='')
    mobile_signals = models.CharField(null=True,max_length=200, default='')
    bus_stand = models.CharField(null=True,max_length=200, default='')
    railway_station = models.CharField(null=True,max_length=200, default='')
    airport = models.CharField(null=True,max_length=200, default='')

    local_govt_authority = models.TextField(default='')

    Summit_Coordinates = models.CharField(null=True, blank=True, max_length=120, default='')
    Base_Village1_Coordinates = models.CharField(null=True, blank=True, max_length=120, default='')
    Base_Village2_Coordinates = models.CharField(null=True, blank=True, max_length=120, default='')
    #latitude=models.FloatField(null=False,blank=False)
    #longitude=models.FloatField(null=False,blank=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    link = models.URLField(null=True, blank=True, default='')

    open_timings = models.TextField(default='Let us know if you have been here..')
    weather_details = models.TextField(default='Let us know if you have been here..')
    govt_guidelines = models.TextField(default='Let us know if you have been here..')
    commonly_visited_from = models.TextField(default='Let us know if you have been here..')
    popular_route = models.TextField(default='Let us know if you have been here..')
    languages_spoken = models.TextField(default='Let us know if you have been here..')
    duration_of_visit =models.CharField(max_length=50, default='Let us know if you have been here..')
    hospital = models.TextField(default='Let us know if you have been here..')
    petrol_pump = models.TextField(default='Let us know if you have been here..')

class Place_report(models.Model):
    user_id=models.ForeignKey(People,on_delete=models.CASCADE,related_name='report_people')
    place_id=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='report_place')
    heading = models.CharField(null=True, max_length=120, default='')
    ex_info = models.TextField(null=True ,default='')

class New_place(models.Model):
    #place_id=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='New_place')
    user_id=models.ForeignKey(People,on_delete=models.CASCADE,related_name='New_people')
    data = JSONField()




