from django.db import models
from location_field.models.plain import PlainLocationField
from geosimple import GeohashField, GeoManager
 
# Create your models here.

class states(models.Model):
	city = models.CharField(max_length=255,default="null")
	locations = PlainLocationField(based_fields=['city'], zoom=7)
	places=models.ManyToManyField("posts.Place",default="")
	location = GeohashField()
	objectss = GeoManager()

	def save(self):
		pointlist=str(self.locations).split(",")
		self.location=(float(pointlist[0]),float(pointlist[1]))
		print(self.location)
		super().save()

	def __str__(self):
		return self.city




class hobbytag(models.Model):
	name=models.CharField(max_length=20)
	statename=models.ManyToManyField(states)
	photo=models.ImageField(blank=True,default="")
	#extra_tags=models.ManyToManyField(extra_tag,default="")
	places=models.ManyToManyField("posts.Place",default="")
	def __str__(self):
		return self.name
		
class extra_tag(models.Model):
	name=models.CharField(max_length=20,default="")
	hobbytages=models.ManyToManyField(hobbytag,default="")
	#statetages=models.ManyToManyField(states,default="")
	places=models.ManyToManyField("posts.Place",default="")
	def __str__(self):
		return self.name

class features(models.Model):
	name =models.CharField(max_length=20)
	def __str__(self):
		return self.name
	


	  
		
