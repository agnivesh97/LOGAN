from django.db import models
from location_field.models.plain import PlainLocationField
import posts
from posts import models as placedata
from geosimple import GeohashField, GeoManager
 
# Create your models here.

class state(models.Model):
	city = models.CharField(max_length=255,default="null")
	locations = PlainLocationField(based_fields=['city'], zoom=7)
	places=models.ManyToManyField(placedata.Place,default="")
	
	def __str__(self):
		return self.city  

class hobbytags(models.Model):
	name=models.CharField(max_length=20)
	statename=models.ManyToManyField(states)
	def __str__(self):
		return self.name

class feature(models.Model):
	name =models.CharField(max_length=20)
	def __str__(self):
		return self.name
	

class extra_tags(models.Model):
	name=models.CharField(max_length=20,default="")
	def __str__(self):
		return self.name
	  
		
