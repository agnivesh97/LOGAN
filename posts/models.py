from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from location_field.models.plain import PlainLocationField
from PIL import Image
from django.contrib.postgres.fields import JSONField


# Create your models here.

#from .common import hobbytag
from watson.admin import SearchAdmin
from django.shortcuts import get_object_or_404
from location_field.models.plain import PlainLocationField
from geosimple import GeohashField, GeoManager




class Place(models.Model):
	place_id=models.AutoField(primary_key=True)
	title = models.CharField(max_length=120)
	title_location = models.CharField(max_length=120,default="fill it")
	category = models.CharField(max_length=400, default='Enter trek type, e.g. Himalyan Trek, Western Ghats Trek etc')
	region = models.CharField(max_length=120, default='Let us know if you have been here..')
	locations = PlainLocationField(based_fields=['title_location'], zoom=7)
	#places=models.ManyToManyField("posts.Place",default="")
	Summit_Coordinates = GeohashField()
	objects = GeoManager()



	#Post_List_img = models.FileField(null=True, blank=True)
	Cover_Pic = models.FileField(null=True, blank=True)
	#Content_Pic = models.ForeignKey(Photos)
	#Video_Link = models.CharField(null=True, blank=True, max_length=400, default='null')
	about_the_trek = models.TextField(default='Let us know if you have been here..')
	highest_altitude = models.CharField(max_length=120, default='Edit if you have been here..')
	state= models.CharField(max_length=50, default='Edit if you have been here..')
	wildlife_reserve = models.CharField(max_length=120, default='Edit if you have been here..')
	best_time = models.TextField(default='Edit if you have been here..')
	exploration_spots = models.TextField(default='Edit if you have been here..')
	hardness = models.TextField(default='Let us know if you have been here..')

	trail_highlights = models.TextField(default='Let us know if you have been here..')
	
	
	
	trek_duration = models.CharField(max_length=120, default='Let us know if you have been here..')
	trek_length = models.CharField(max_length=120, default='Let us know if you have been here..')
	endurance_level = models.CharField(max_length=120, default='Let us know if you have been here..')
	difficulty = models.CharField(max_length=120, default='Let us know if you have been here..')

	route_to_base_camp = models.CharField(max_length=120, default='Let us know if you have been here..')
	route_details = models.TextField(default='Let us know if you have been here..')
	base_village = models.CharField(max_length=120, default='Enter Base Vilage Here..')
	summit_point = models.CharField(max_length=120, default='Enter Base Vilage Here..')
	trek_route = models.TextField(default='Let us know if you have been here..')
	
	
	food_tips = models.TextField(default='Let us know if you have been here..')
	water_tips = models.TextField(default='Let us know if you have been here..')
	stay_tips = models.TextField(default='Let us know if you have been here..')
	equipments_tips = models.TextField(default='Let us know if you have been here..')
	fitness_tips = models.TextField(default='Let us know if you have been here..')
	permissions = models.TextField(default='Let us know if you have been here..')

	accomodation = models.TextField(default='Let us know if you have been here..')

	
	police_station = models.CharField(max_length=200, default='Let us know if you have been here..')
	atm = models.CharField(max_length=200, default='Let us know if you have been here..')
	mobile_signals = models.CharField(max_length=200, default='Let us know if you have been here..')
	railway_station = models.CharField(max_length=200, default='Let us know if you have been here..')
	airport = models.CharField(max_length=200, default='Let us know if you have been here..')
	hospital = models.TextField(default='Let us know if you have been here..')
	atm = models.TextField(default='Let us know if you have been here..')
	bus_stand = models.CharField(max_length=200, default='Let us know if you have been here..')
	petrol_pump = models.TextField(default='Let us know if you have been here..')
	mobile_signals = models.TextField(default='Let us know if you have been here..')
	service_station = models.TextField(default='Let us know if you have been here..')
	local_govt_authority = models.TextField(default='Let us know if you have been here..')

	#Summit_Coordinates = models.CharField(null=True, blank=True, max_length=120, default='null')
	Base_Village1_Coordinates = models.CharField(null=True, blank=True, max_length=120, default='null')
	Base_Village2_Coordinates = models.CharField(null=True, blank=True, max_length=120, default='null')
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	
	link = models.URLField(null=True, blank=True, default='')

	open_timings = models.TextField(default='Edit if you have been here..')
	weather_details = models.TextField(default='Edit if you have been here..')
	govt_guidelines = models.TextField(default='Edit if you have been here..')
	commonly_visited_from = models.TextField(default='Let us know if you have been here..')
	popular_route = models.TextField(default='Let us know if you have been here..')
	languages_spoken = models.TextField(default='Let us know if you have been here..')
	duration_of_visit =models.CharField(max_length=50, default='Let us know if you have been here..')
   
	#hobby_tages=models.TextField(default='Let us know if you have been here..')
	
	def __str__(self):
		return self.title

	def save(self):
		pointlist=str(self.locations).split(",")
		if self.title_location=="":
			self.title_location=self.title
		self.Summit_Coordinates=(float(pointlist[0]),float(pointlist[1]))
		print(self.Summit_Coordinates)
		#super().save()
			
		#print(self.location)
		super().save()








class People(models.Model):

	peopleid=models.AutoField(primary_key=True)
	username=models.CharField(max_length=200,blank=False,null=False)
	password=models.CharField(max_length=200,blank=False,null=False)
	aboutme=models.CharField(max_length=200,blank=False,null=False,default="The user is yet to update")
	email=models.EmailField(max_length=200,blank=False,null=False)
	photo=models.URLField(max_length=200,default='/media/avt.png')
	point=models.CharField(max_length=10,default=0)
	userid=models.CharField(max_length=50,default=0)
	adminpoint=models.CharField(max_length=10,default=0)
	manytomanypeopleid=models.ManyToManyField("self",default="",null=True)
	manytomanyplaceid=models.ManyToManyField(Place,default="",null=True)
	manytomanyplacetype=models.ManyToManyField("PlaceType",default="",null=True)
	manytomanyarticlestatusid=models.ManyToManyField("People_Article_Status",null=True)
	manytomanyphotopoststatusid=models.ManyToManyField("People_Photo_Post_Status",null=True)
	manytomanytripstatusid=models.ManyToManyField("People_Trips_Status",null=True)
	manytomanyquestionstatusid=models.ManyToManyField("People_Question_Status")
	manytomanyanswerstatusid=models.ManyToManyField("People_Answer_Status",null=True)
	manytomanyreviewstatusid=models.ManyToManyField("Review_place_status",null=True)
	manytomanytipstatusid=models.ManyToManyField("People_Tips_Status",null=True)
	def __str__(self):
		return str(self.peopleid)


class Adminlogin(models.Model):
	username=models.CharField(max_length=10,blank=False,null=False)
	password=models.CharField(max_length=10,blank=False,null=False)
	def __str__(self):
		return str(self.username)

class PlaceType(models.Model):
	placetype=models.CharField(max_length=2,blank=False,null=False)
	place=models.ForeignKey(Place, on_delete=models.CASCADE)
	#place=models.ForeignKey(People, on_delete=models.CASCADE,related_name='people_like_type')
	def __str__(self):
		return str(self.placetype+" "+str(self.place))


class Place_Follow(models.Model):
	place_id=models.ForeignKey(Place,on_delete=models.CASCADE)
	follow_id=models.ForeignKey(People,on_delete=models.CASCADE)

class Photos(models.Model):
	photoid=models.AutoField(primary_key=True)
	photo=models.ImageField(null=False,blank=True)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	rating=models.FloatField(null=False,default="1")
	userid=models.ForeignKey(People,on_delete=models.CASCADE)

	def save(self, size=(600, 400)):
		max_=1500
		
		if not self.photoid and not self.photo:
			return            
		newwidth=0
		newheight=0
		super(Photos, self).save()

		image = Image.open(self.photo)
		width, height = image.size
		if width>max_:
			newwidth=max_
			newheight=int(max_*height/width)
			if newheight>max_:
				newheight=max_
				newwidth=int(max_*width/height)
		elif height>max_:
			newheight=max_
			newwidth=int(max_*width/height)
			if newwidth>max_:
				newwidth=max_
				newheight=int(max_*height/width)
		else:
			newwidth=width
			newheight=height
		size=(newwidth,newheight)
		image=image.resize(size, Image.ANTIALIAS)
		image.save(self.photo.path)
	def __str__(self):
		return str(self.photoid)

class Videos(models.Model):
	videoid=models.AutoField(primary_key=True)
	video=models.URLField(null=True,blank=True)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	rating=models.FloatField(null=False)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)


class People_Place(models.Model):
	place_id=models.ForeignKey(Place, on_delete=models.CASCADE)
	user_id=models.ForeignKey(People,on_delete=models.CASCADE)
	details=models.CharField(max_length=5000,blank=True,null=False)
	#video_id=models.ForeignKey(Videos,on_delete=models.CASCADE)

class People_Question(models.Model):
	quesid=models.AutoField(primary_key=True)
	questiontext=models.CharField(max_length=5000,null=False,blank=False)
	place_id=models.ForeignKey(Place,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	#time=models.DateTimeField(auto_now=True, auto_now_add=False)
	def __str__(self):
		return str(self.quesid)




class People_Answer(models.Model):
	answerid=models.AutoField(primary_key=True)
	answertext=models.CharField(max_length=5000,null=False,blank=False)
	answerquesid=models.ForeignKey(People_Question, on_delete=models.CASCADE)
	userid=models.ForeignKey(People, on_delete=models.CASCADE)
	placeid=models.ForeignKey(Place, on_delete=models.CASCADE)
	time=models.DateTimeField(auto_now=True,auto_now_add=False)
	def __str__(self):
		return str(self.answerid)


class People_Question_Status(models.Model):
	#people_questions=models.AutoField(primary_key=True)
	quesid=models.ForeignKey(People_Question, on_delete=models.CASCADE)
	status=models.BooleanField(default=False)
	userid=models.ForeignKey(People, on_delete=models.CASCADE)
	placeid=models.ForeignKey(Place , on_delete=models.CASCADE)
	report=models.CharField(max_length=20,default='none',blank=True,null=False)

	def __str__(self):
		return ("Report is "+str(self.report)+" Status is "+str(self.status))

	def save(self):
		super().save()
		try:
			user=People_Question_Status.objects.get(id=self.id).quesid.userid
			try :
				obj=user.manytomanyquestionstatusid.get(id=self.id)
			except Exception as e:
				print(e)
				user.manytomanyquestionstatusid.add(self.id)
		except Exception as e:
			print(e)

class People_Question_Report(models.Model):
	reportid=models.AutoField(primary_key=True)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	reportstatus=models.CharField(max_length=50,null=False,blank=False)

class People_Answer_Status(models.Model):
	answerid=models.ForeignKey(People_Answer, on_delete=models.CASCADE)
	questionid=models.ForeignKey(People_Question, on_delete=models.CASCADE)
	placeid=models.ForeignKey(Place, on_delete=models.CASCADE)
	userid=models.ForeignKey(People, on_delete=models.CASCADE)
	answerstatus=models.BooleanField(default=False)
	answerreport = models.CharField(max_length=20, default='none', blank=True, null=False)
	def save(self):
		super().save()
		try:
			user=People_Answer_Status.objects.get(id=self.id).answerid.userid
			try :
				obj=user.manytomanyanswerstatusid.get(id=self.id)
			except Exception as e:
				print(e)
				user.manytomanyanswerstatusid.add(self.id)
		except Exception as e:
			print(e)


class Review_place(models.Model):
	review_id=models.AutoField(primary_key=True)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	review_text=models.CharField(max_length=5000,null=False,blank=False)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	dateandtime=models.DateField(auto_now=True,auto_now_add=False)
	def __str__(self):
		return self.review_text

class Review_place_status(models.Model):
	review_status_id=models.AutoField(primary_key=True)
	review_id=models.ForeignKey(Review_place,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	helpful=models.BooleanField(max_length=50,default=False,blank=True,null=False)
	report=models.CharField(max_length=20,default='none',blank=True,null=False)
	def __str__(self):
		return self.report+" and helpful="+str(self.helpful)

	def save(self):
		super().save()
		try:
			user=Review_place_status.objects.get(review_status_id=self.review_status_id).review_id.userid
			try :
				obj=user.manytomanyreviewstatusid.get(review_status_id=self.review_status_id)
			except Exception as e:
				print(e)
				user.manytomanyreviewstatusid.add(self.review_status_id)
		except Exception as e:
			print(e)

class Admin_notification(models.Model):
	nid=models.AutoField(primary_key=True)
	notification=models.CharField(max_length=500,blank=True,null=False)
	category=models.CharField(max_length=100,blank=True,null=True)
	def __str__(self):
		return "["+self.category+"]:"+self.notification

class People_Article(models.Model):
	articleid=models.AutoField(primary_key=True)
	articletext=models.CharField(max_length=5000,null=False,blank=False)
	#photoid=models.ForeignKey(Photos, on_delete=models.CASCADE)
	userid=models.ForeignKey(People, on_delete=models.CASCADE)
	ratings=models.FloatField()
	article_title=models.CharField(max_length=500,default="")
	time=models.DateTimeField(auto_now=True, auto_now_add=False)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE,default=6)
	type=models.CharField(max_length=250,null=False,blank=False,default="")
	hobbytags=models.ManyToManyField("search_app.hobbytag",default="",null=True)

	def __str__(self):
		return str(self.articleid)

class People_Article_Comment(models.Model):
	commentid=models.AutoField(primary_key=True)
	articlecommentid=models.ForeignKey(People_Article,on_delete=models.CASCADE)
	#photoid=models.ForeignKey(Photos,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	#placeid=models.ForeignKey(Place,on_delete=models.CASCADE,default=6)
	commenttext=models.CharField(max_length=5000,null=False,blank=True)



class People_Article_Status(models.Model):
	articleid=models.ForeignKey(People_Article,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	status=models.CharField(max_length=20, default='none', blank=True, null=False)


	def save(self):
		super().save()
		try:
			user=People_Article.objects.get(articleid=self.articleid).userid
			try :
				obj=user.manytomanyarticlestatusid.get(id=self.id)
			except Exception as e:
				print(e)
				user.manytomanyarticlestatusid.add(self.id)
		except Exception as e:
			print(e)
	
	#placeid = models.ForeignKey(Place, on_delete=models.CASCADE,default=6)

class People_Article_Comment_Status(models.Model):

	articlecommentid=models.ForeignKey(People_Article_Comment,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	articleid=models.ForeignKey(People_Article,on_delete=models.CASCADE)
	status=models.CharField(max_length=50,null=False,blank=True)



class Tag(models.Model):
	tagid=models.AutoField(primary_key=True)
	tagname=models.CharField(max_length=1000,null=False,blank=True)

	def __str__(self):
		return self.tagname

class Tag_Article(models.Model):
	tagid=models.ForeignKey(Tag,on_delete=models.CASCADE)
	articleid=models.ForeignKey(People_Article,on_delete=models.CASCADE)


class YourModelAdmin(SearchAdmin):

	search_fields = ("title", "place_id")


class People_Photo_Post(models.Model):
	photopostid=models.AutoField(primary_key=True)
	photoposttext=models.CharField(max_length=5000,null=True,blank=True)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	ratings=models.FloatField(default=1)
	time = models.DateTimeField(auto_now=True, auto_now_add=False)
	photosimg=models.ManyToManyField("photos")
	def __str__(self):
		return str(self.photopostid)


class People_Trips(models.Model):
	tripid=models.AutoField(primary_key=True)
	#trip_location=models.CharField(max_length=1000,null=False,blank=False)
	traveling_from=models.CharField(max_length=1000,null=False,blank=False)
	traveling_to=models.CharField(max_length=1000,null=False,blank=False)

	travel_starting_date=models.DateField()
	travel_ending_date=models.DateField()
	nooftravelerscurrent=models.IntegerField()
	nooftravelersrequired=models.IntegerField()
	preferences=models.CharField(max_length=5000,null=False,blank=False)
	trip_planning=models.CharField(max_length=5000,null=False,blank=False)
	expenses_details=models.CharField(max_length=2000,null=False,blank=False)
	phone_number=models.IntegerField()
	email=models.EmailField()
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	time=models.DateTimeField(auto_now=True,auto_now_add=False)

	def __str__(self):
		return str(self.tripid)


class People_Photo_Post_Status(models.Model):
	photopostid=models.ForeignKey(People_Photo_Post,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	#placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	status = models.CharField(max_length=1000, null=False, blank=False,default="none")
	report = models.CharField(max_length=20, default='none', blank=True, null=False)

	def save(self):
		super().save()
		try:

			usid=People_Photo_Post_Status.objects.get(id=self.id).photopostid.userid
			user=usid
			print(user)
			try :
				obj=user.manytomanyphotopoststatusid.get(id=self.id)
			except Exception as e:
				print(e)
				user.manytomanyphotopoststatusid.add(self.id)
		except Exception as e:

			print(e)


	#photosuperstatus=models.BooleanField(default=False)


class People_Photo_Post_Comment(models.Model):
	photocommentid=models.AutoField(primary_key=True)
	photopostid=models.ForeignKey(People_Photo_Post,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	#placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	photocomment=models.CharField(max_length=5000,null=False,blank=False)

class People_Trips_Status(models.Model):
	tripid=models.ForeignKey(People_Trips,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
   # placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	status = models.CharField(max_length=1000, null=False, blank=False,default="none")
	report = models.CharField(max_length=20, default='none', blank=True, null=False)

	def save(self):
		super().save()
		try:
			user=People_Trips_Status.objects.get(id=self.id).tripid.userid
			try :
				obj=user.manytomanytripstatusid.get(id=self.id)
			except Exception as e:
				print(e)
				user.manytomanytripstatusid.add(self.id)
		except Exception as e:
			print(e)

	#superstatus=models.BooleanField(default=False)

class People_Trips_Comment(models.Model):
	tripcommentid=models.AutoField(primary_key=True)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	#placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	tripid=models.ForeignKey(People_Trips,on_delete=models.CASCADE)
	comment=models.CharField(max_length=5000,null=False,blank=False)



	
	
class Place_t(models.Model):
	parent_place = models.ForeignKey('self', null=True, blank=True)
	city = models.CharField(max_length=255)
	location = PlainLocationField(based_fields=['city'], zoom=7)





class People_Tips(models.Model):
	tipid=models.AutoField(primary_key=True)
	tiptitle=models.CharField(max_length=500,blank=True,null=True)
	tipdetails=models.CharField(max_length=1000,blank=False,null=False)
	placeid=models.ForeignKey(Place,on_delete=models.CASCADE)
	tipuserid=models.ForeignKey(People,on_delete=models.CASCADE)
	time=models.DateTimeField(auto_now=True,auto_now_add=False)
	#no_helpful=models.IntegerField(default=0)

class People_Tips_Status(models.Model):
	tipstatusid=models.AutoField(primary_key=True)
	tipid=models.ForeignKey(People_Tips,on_delete=models.CASCADE)
	userid=models.ForeignKey(People,on_delete=models.CASCADE)
	status=models.BooleanField(max_length=10,default=False,blank=True,null=False)
	report=models.CharField(max_length=50,default='none',blank=True,null=False)

	def save(self):
		super().save()
		try:
			user=People_Tips_Status.objects.get(tipstatusid=self.tipstatusid).tipid.tipuserid
			try :
				obj=user.manytomanytipstatusid.get(tipstatusid=self.tipstatusid)
			except Exception as e:
				print(e)
				user.manytomanytipstatusid.add(self.tipstatusid)
		except Exception as e:
			print(e)


class conversation(models.Model):
	cid=models.AutoField(primary_key=True)
	senderid=models.ForeignKey(People,on_delete=models.CASCADE,related_name='senderid')
	receiverid=models.ForeignKey(People,on_delete=models.CASCADE,related_name='receiverid')

	def __str__(self):
		return str(self.cid)


class message(models.Model):
	mid=models.AutoField(primary_key=True)
	cid=models.ForeignKey(conversation,on_delete=models.CASCADE)
	msgsenderid=models.ForeignKey(People,on_delete=models.CASCADE,related_name='msgsenderid')
	msgreceiverid=models.ForeignKey(People,on_delete=models.CASCADE,related_name='msgreceiverid')
	reply=models.CharField(max_length=5000,blank=False,null=True)

	def __str__(self):
		return str(self.reply)


	
class Join_table(models.Model):
	post_photo=models.ForeignKey(People_Photo_Post,null=True, blank=True,default="")
	post_trips=models.ForeignKey(People_Trips,null=True, blank=True,default="")
	post_article=models.ForeignKey(People_Article,null=True, blank=True,default="")
	post_tip=models.ForeignKey(People_Tips,null=True, blank=True,default="")
	time=models.DateTimeField(auto_now=True,auto_now_add=False)


class User_record(models.Model):
    place_id=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='Reu_place')
    user_id=models.ForeignKey(People,on_delete=models.CASCADE,related_name='Reu_people')
    data = JSONField()

class user_profile_pic(models.Model):
	user_id=models.ForeignKey(People,on_delete=models.CASCADE,related_name='pic_people')
	photo=models.ImageField(null=False,blank=True)
	def save(self, size=(600, 400)):
		max_=1500
		
		if not self.id and not self.photo:
			return            
		newwidth=0
		newheight=0
		super(user_profile_pic, self).save()

		image = Image.open(self.photo)
		width, height = image.size
		if width>max_:
			newwidth=max_
			newheight=int(max_*height/width)
			if newheight>max_:
				newheight=max_
				newwidth=int(max_*width/height)
		elif height>max_:
			newheight=max_
			newwidth=int(max_*width/height)
			if newwidth>max_:
				newwidth=max_
				newheight=int(max_*height/width)
		else:
			newwidth=width
			newheight=height
		size=(newwidth,newheight)
		image=image.resize(size, Image.ANTIALIAS)
		image.save(self.photo.path)
		user=self.user_id
		user.photo="/media/" + str(self.photo)
		user.save()
	def __str__(self):
		return str(self.id)


    
	

