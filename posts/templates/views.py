from urllib.parse import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from passlib.hash import pbkdf2_sha256
from django.contrib import messages
from django.http import JsonResponse
import edite_data
from edite_data.models import *
from django.core.serializers import json
import json
from watson import search as watson
import time
from django.contrib.gis.geoip import GeoIP
import search_app 
from search_app import models as search_model
from search_app.views import place_search
from googleplaces import GooglePlaces, types, lang
from collections import OrderedDict

def get_place_photo(request):
	placeid = json.loads(request.body.decode('utf-8'))['placeid']
	return JsonResponse({"photo_url":get_photo(placeid,2)},safe=False)


def get_photo(placeid,no):

	YOUR_API_KEY = 'AIzaSyDdU_KsgaJdnlLhDepXnX2_6JCwBidaU5w'
	place_obj=Place.objects.get(place_id=placeid)
	title=place_obj.title
	print(title)
	google_places = GooglePlaces(YOUR_API_KEY)

	# You may prefer to use the text_search API, instead.
	query_result = google_places.nearby_search(
			location=title+' , India', radius=2000,name=title)
	# If types param contains only 1 item the request to Google Places API
	# will be send as type param to fullfil:
	# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html
	photo_url=[]
	if query_result.has_attributions:
		i=0

	for place in query_result.places:
		if len(photo_url)>no:
			break
		place.get_details()
		#print (place.details) # A dict matching the JSON response from Google.

		# Getting place photos

		for photo in place.photos:
			if len(photo_url)>no:
				break
			
			photo.get(maxheight=500, maxwidth=500)
			
			try:
				print(photo.url)
				photo_url.append(photo.url)
			except Exception as e:
				print(e)
				break
			
			# Original filename (optional)
			#photo.filename
			# Raw image data
			#photo.data
	return photo_url



def post_home(request, id=None):
	context={}
	username=None
	if request.session.get("sessionid",None):
		sessionid=request.session["sessionid"]
		context["sessionid"]=sessionid
		username=People.objects.get(peopleid=sessionid).username
		context["pic"]=request.session["sessionpic"]
		
	places = Place.objects.all().values('place_id','title','Cover_Pic')
	context["loginForm"]=LoginForm()
	context["registerForm"]=RegistrationForm()
	context["places"]=places
	context["username"]=username


	return render(request, "posts/index.html",context)

def user_location(request):
	lat=request.GET.get('latitude')
	lng=request.GET.get('longitude')
	points=[]
	points.append(lat)
	points.append(lng)
	request.session["location"]=points
	print(request.session["location"])
	return HttpResponse()




def post_detail(request, id=None):
	sessionid=None
	print(id)
	instance = get_object_or_404(Place, title=id)
	status=False
	status1=False
	status2=False
	user_obj=None
	places_visited=0
	places_wished=0
	places_follow=0
	follower=0
	if request.session.get('sessionid',None):
		sessionid=request.session["sessionid"]
		user_obj=People.objects.get(peopleid=sessionid)
		if user_obj.manytomanyplacetype.filter(place=instance,placetype=0):
			status=True
		if user_obj.manytomanyplacetype.filter(place=instance,placetype=1):
			status1=True
		if user_obj.manytomanyplacetype.filter(place=instance,placetype=2):
			status2=True
		places_visited=user_obj.manytomanyplacetype.filter(placetype=1).count()
		places_wished=user_obj.manytomanyplacetype.filter(placetype=2).count()
		places_follow=user_obj.manytomanyplacetype.filter(placetype=0).count()
		follower=user_obj.manytomanypeopleid.all().count()
	
	i=0		
	color=["#008489","#008489","#008489","#008489"]
	tag_list=[]
	icounter=0
	hobby_tag_list=instance.hobbytag_set.all()
	for hobbytag_obj in hobby_tag_list:
		temp={}
		count=i%4
		temp["color"]=color[count]
		temp["tagname"]=hobbytag_obj.name
		tag_list.append(temp)
		i=i+1


	try:

		temp_list=(instance.category).split(",")
		for te in temp_list:
			temp={}
			count=i%4
			temp["color"]=color[count]
			temp["tagname"]=te
			tag_list.append(temp)
			print(tag_list)
			i=i+1
	except Exception as e:
		print(e)
		i=0


	#print("gadbad statussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
	print (status2)
	share_string = quote_plus(instance.title)
	#print(instance.place_id)
	gernal_info=OrderedDict()
	gernal_info['About This Place']=instance.about_the_trek  
	#gernal_info['Highest Altitude']=instance.highest_altitude
	gernal_info['Location']=instance.state
	#gernal_info['Wildlife Reserve']=instance.wildlife_reserve
	gernal_info['Best Time to Visit']=instance.best_time
	gernal_info['Open Timings']=instance.open_timings
	#gernal_info['Weather Details']=instance.weather_details
	gernal_info['Govt. Guidelines']=instance.govt_guidelines
	gernal_info['Languages Spoken']=instance.languages_spoken
	
	#gernal_info['Hardness']=instance.hardness
	print(gernal_info)
	tips={}
	tips1={}
	tips["Commonly Visited From"]=instance.commonly_visited_from
	tips["Popular Route"]=instance.popular_route
	tips1["RailwayStation"]=instance.railway_station
	tips1["BusStation"]=instance.bus_stand
	tips1["Airport"]=instance.airport
	#tips["For Stay"]=instance.stay_tips
	#tips["For Fitness"]=instance.fitness_tips
	#tips["Things To Carry"]=instance.equipments_tips
	#tips["Special Permissions"]=instance.permissions
	
	trails={}
	trails["Trail Route"]=instance.trek_route
	trails["Trail Highlights"]=instance.trail_highlights
	
	basecampe={}
	basecampe["Onwards"]="NO"
	basecampe["Route Details"]="NO"
	
	emergency_locations={}
	emergency_locations["Police Station"]=instance.police_station
	#emergency_locations["Railway Station"]=instance.railway_station
	emergency_locations["Hospital"]=instance.hospital
	emergency_locations["Last ATM"]=instance.atm
	#emergency_locations["Airport"]=instance.airport
	#emergency_locations["Bus/Taxi Station"]=instance.bus_stand
	emergency_locations["Petrol Pump"]=instance.petrol_pump
	emergency_locations["Mobile Signals"]=instance.mobile_signals
	#emergency_locations["Service Station"]=instance.service_station
	if user_obj:
		username=user_obj.username
	else:
		username=""


	context = {
		
		"instance" : instance,
		"gernal_info" : gernal_info,
		"food" : tips,
		"food1" : tips1,
		"trails" :trails,
		"basecampe":basecampe,
		"emergency_locations":emergency_locations,
		"placeid":instance.place_id,
		"sessionid":sessionid,
		"status":status,
		"status1":status1,
		"status2":status2,
		"tag_list":tag_list,
		"placefollowers":People.objects.filter(manytomanyplacetype__placetype='0',manytomanyplacetype__place=instance).count(),
		"placebeenher":People.objects.filter(manytomanyplacetype__placetype='1',manytomanyplacetype__place=instance).count(),
		"placerecommended":People.objects.filter(manytomanyplacetype__placetype='2',manytomanyplacetype__place=instance).count(),
		"username":username,
		"loginForm":LoginForm(),
		"registerForm":RegistrationForm(),
		"places_visited":places_visited,
		"places_wished":places_wished,
		"places_follow":places_follow,
		"follower":follower
		#"pic":request.session['sessionpic']
	}

	if request.session.get("sessionpic",None):
		context["pic"]=request.session['sessionpic']
	
	#print(context)
	return render(request,"posts/postdetails.html", context)

def post_list(request):
	
	if not request.session.get('sessionid',None):
		i=0
		#messages.info(request, 'Required')
		#return HttpResponseRedirect('/')


	queryset_list= Place.objects.all()

	query = request.GET.get("q")
	
	if query:
		print("hello")
	queryset_list = queryset_list.filter(
		Q(title__icontains="place")
			).distinct()

	paginator = Paginator(queryset_list, 20) # Show 25 contacts per page
	photos=Photos.objects.values_list('photo', flat=True).all()
	print(photos)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	
	context = {
		"object_list": queryset,
		"title" : "List",
		"photos" : photos,
		#"pic":request.session['sessionpic']
	}
	if request.session.get("sessionpic",None):
		context["pic"]=request.session['sessionpic']
		
	return render(request, "posts/base.html", context)


def post_update(request):
	return HttpResponse("<h1>update</h1>")

def post_delete(request):
	return HttpResponse("<h1>delete</h1>")
def homep(request):
	return HttpResponseRedirect("/")
# Create your views here.
def photolink(request):
	try:

		username=None
		if request.session.get('sessionid',None):
			sessionid=request.session["sessionid"]
			username=People.objects.get(peopleid=sessionid).username 
			i=0
		context={}
		search_query=request.GET.get('q',None)
		print(search_query) 
		try:

			place_obj=Place.objects.get(title=search_query)
			return redirect("/place/"+place_obj.title+"/")
		except Exception as e:
			people_obj=People.objects.filter(username=search_query)
			if people_obj:
				context={"object_list":people_obj}
				return render(request, "posts/base.html", context)

		if search_query:
			hobby_tag=search_in_waston(search_query.split(" "),search_model.hobbytag)
			#print(hobby_tag)
			context["hobby_tag"]=(hobby_tag[0].first()).name
			context["search_text"]=search_query
			#print(search_query)

		hobby_tag_list=search_model.hobbytag.objects.all()	
		if request.session.get("sessionpic",None):
			context["pic"]=request.session['sessionpic']

		context["loginForm"]=LoginForm()
		context["registerForm"]=RegistrationForm()
		context["hobby_tag_list"]=hobby_tag_list
		context["username"]=username

		return render(request, "posts/LOGAN.html", context)
	except Exception as e:
		if request.session.get("sessionpic",None):
			context["pic"]=request.session['sessionpic']
		return render(request, "posts/404.html",context)








def search(request):
	search_text=json.loads(request.body.decode('utf-8'))['search']
	sub_tag=[]
	#your_queryset = Place.objects.all().values('title','place_id')
	if 'hobbytag' in search_text.keys():
		hobby_tag=search_model.hobbytag.objects.filter(name=search_text["hobbytag"]).first()
		place_list=hobby_tag.places.all()
		#print(hobby_tag)
		if 'extratag' in search_text.keys():
			place_list=(search_in_waston(search_text['extratag'].split(" "),place_list))[0]
		#print(place_list)
		extratags=list(search_model.extra_tag.objects.filter(hobbytages__name=hobby_tag.name).values("name"))
		sub_tag=extratags
		#print(extratags)
	else:
		place_list=Place.objects.all()


	place_data=[]
	i = 0
	for place in place_list:
		temp={}
		#print("sahkjhsadsahkj")


		
		try:
			point=place.Summit_Coordinates.as_tuple()
			#print(point)
			
			print(str(point)[1:-2])
			temp["coordinates"]=str(point)[1:-2]
			temp["placename"]=place.title
			temp["place_id"]=place.place_id
			temp["noofdays"]=place.trek_length
		
		except Exception as e:
			temp["coordinates"]="18.001,23.000001"
			temp["placename"]=place.title
			temp["place_id"]=place.place_id
			temp["noofdays"]=place.trek_length

		#print(i)
		#ph=Photos.objects.filter(placeid__place_id=5).values().first()
		#print(str(ph))
		try:
			photoname=str(place.Cover_Pic.url)
		except Exception as e:
			print(e)
			photoname="nopic"

		temp["photo"]=photoname
		temp["place_no"]=i
		place_data.append(temp)
		i=i+1
	context = {
		"data": place_data,
		"extratags":sub_tag,
		}
	#print(context)
	return HttpResponse(JsonResponse(context))


def get_hobbytags(request):
	hobbytag_obj_list=search_model.hobbytag.objects.all()
	context_list=[]
	for hobbytag_obj in hobbytag_obj_list:
		context_list.append(hobbytag_obj.name)
	print(context_list)
	return JsonResponse(context_list,safe=False)


def index(request):
	context = {}
	context["loginForm"] = LoginForm()
	context["registerForm"] = RegistrationForm()
	return render(request, "posts/login_register.html", context)

def register(request):
	if request.method=="POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			try:
				user_object = get_object_or_404(People, Email = form.cleaned_data["email"])
				messages.info(request, messages.ERROR, 'Email already taken.')
				#return HttpResponseRedirect("/")
			except Exception as e:
				if form.cleaned_data["confirm_password"]==form.cleaned_data["password"]:

					hash = pbkdf2_sha256.encrypt(form.cleaned_data["password"], rounds=200000, salt_size=32)
					entry = People(
							username=form.cleaned_data["username"],
							email=form.cleaned_data["email"],
							password=hash,
							)
					entry.save()

					messages.info(request, messages.SUCCESS,'Successfully Registered. Login with the email and password.')

					if request.GET.get("q",None):
						return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
					else:
						print("q2")
						return HttpResponseRedirect("/")
				else:
					messages.info(request, messages.ERROR,'Password Mismatch')
					if request.GET.get("q",None):
						return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
					else:
						print("q2")
						return HttpResponseRedirect("/")
		else:
			messages.info(request, messages.ERROR, 'Form Error. Stop tampering with the form')
			if request.GET.get("q",None):
				return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
			else:
				return HttpResponseRedirect("/")
	else:
		messages.add_message(request, messages.ERROR, 'Not a valid POST request.')
		return HttpResponse("<script>alert(messages)</script>")





def login_(request):
	if  request.method=="POST":
		Login_Form = LoginForm(request.POST)
		if Login_Form.is_valid():
			try:
				#print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
				#hash=pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(Login_Form.cleaned_data["password"])
				profile_object=People.objects.get(email=Login_Form.cleaned_data["email"])
				#print("errorerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
				user_login=pbkdf2_sha256.using(rounds=200000, salt_size=32).verify(Login_Form.cleaned_data["password"], profile_object.password)
			except Exception as e:
				messages.info(request, 'Login Failed')
				print("not login ")
				if request.GET.get("q",None):
					return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
				else:
					print("q2")
					return HttpResponseRedirect("/")

			if user_login:
				request.session["sessionid"]=profile_object.peopleid
				request.session["sessionpic"]=str(profile_object.photo)
				if request.GET.get("q",None):
					return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
				else:
					print("q2")
					return HttpResponseRedirect("/")
			else:
				messages.add_message(request, messages.ERROR, 'Email/Password didn\'t match')
				if request.GET.get("q",None):
					return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
				else:
					print("q2")
					return HttpResponseRedirect("/")


		else:
			messages.info(request, messages.ERROR, 'Form error. Stop tampering with the form.')
			if request.GET.get("q",None):
				return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
			else:
				print("q2")
				return HttpResponseRedirect("/")
	else:
		messages.info(request, messages.ERROR, 'Not a valid POST request.')
		if request.GET.get("q",None):
			return HttpResponseRedirect("/postdetail/"+request.GET["q"]+"/")
		else:
			print("q2")
			return HttpResponseRedirect("/")


def update_place(request,user_id=None):
	id=request.GET.get('placeid')
	text=request.GET.get('text')
	textid=request.GET.get('textid')
	adminpoint=request.GET.get('adminpoint')
	print("temp");
	peopleid=People.objects.get(peopleid=user_id)
	
	userid=request.session.get('sessionid',1)
	try :
		instance=Place.objects.get(place_id=id)
		instance2=Place_temp.objects.get(place_id=instance,user_id=peopleid)
		if textid == "About This Place":
			instance.about_the_trek=text
			instance2.about_the_trek=''

		elif textid == "Highest Altitude":
			instance.highest_altitude=text
			instance2.highest_altitude=''
		elif textid == 'Location':
			instance.state=text
			instance2.state=''
			i=0
		elif textid == 'Wildlife Reserve':
			instance.wildlife_reserve=text
			instance2.wildlife_reserve=""
		elif textid == 'Best Time':
			instance.best_time=text
			instance2.best_time=""
		elif textid == 'What To Explore':
			i=0

		elif textid == "Food":
			i=0
		elif textid == "Accomodations":
			instance.accomodation=text
			instance2.accomodation=""
		elif textid == 'Fitness':
			i=0
		elif textid == 'Equipments':
			i=0
		elif textid == "Trail Route":
			instance.trek_route=text
			instance2.trek_route=""
		elif textid == "Trail Highlights":
			instance.trail_highlights=text
			instance2.trail_highlights=""
		elif textid == "Onwards":
			i=0
		elif textid == 'Route Details':
			i=0
		elif textid == "Police Station":
			instance.police_station=text
			instance2.police_station=""
		elif textid == "ATM":
			instance.atm=text
			instance2.atm=""
		elif textid =="Airport":
			instance.airport=text
			instance2.airport=""
		elif textid == "BusStation":
			instance.bus_stand=text
			instance2.bus_stand=""

		elif textid == "Best Time to Visit":
			instance.best_time=text
			instance2.best_time=""
		elif textid == "Open Timings":
			instance.open_timings=text
			instance2.open_timings=""
		elif textid == "Weather Details":
			instance.weather_details=text
			instance2.weather_details=""
		elif textid == "Govt. Guidelines":
			instance.govt_guidelines=text
			instance2.govt_guidelines=""
		elif textid == "Languages Spoken":
			instance.languages_spoken=text
			instance2.languages_spoken=""
		elif textid == "Commonly Visited From":
			instance.commonly_visited_from=text
			instance2.commonly_visited_from=""
		elif textid == "Popular Route":
			instance.popular_route=text
			instance2.popular_route=""
		instance.save()
		instance2.save()
		data={}
		data['is_taken']=True
		peopleid.adminpoint=int(peopleid.adminpoint)+int(adminpoint)
		peopleid.save()
	except Exception as e:
		data={} 
		data['is_taken']=False
		print(e)
	return JsonResponse(data)






def create_review(request,id=None):
	if request.method=='POST':
		placeid=id
		s=4
		if request.session.get("sessionid",None):
			s=request.session['sessionid']
		#print(placeid)
		#reviewtxt=request.POST['reviewtxt']
		reviewtxt=json.loads(request.body.decode('utf-8'))["review"]
		obj1=People.objects.get(peopleid=s)
		obj2=Place.objects.get(place_id=id)
		userid=obj1.peopleid
		placeid=obj2.place_id
		entry_review_obj=Review_place(userid=obj1,placeid=obj2,review_text=reviewtxt,dateandtime=time.time())
		entry_review_obj.save()
		print(reviewtxt+"value inserted")
		return HttpResponse()
	else:
		return HttpResponse('<script>alert("no")</script>')

def create_reviewStatus(request,id=None):
	if request.method=="POST":
		s=4
		if request.session.get("sessionid",None):
			s=request.session['sessionid']
		obj1=Review_place.objects.get(review_id=id)
		print ("Hello ang status"+str(id))
		#placeid1=obj1.placeid
		try:
			obj2=Review_place_status.objects.get(review_id=id,userid=s)
			if obj2.helpful==True:
				obj2.helpful=False
			else:
				obj2.helpful=True
			obj2.save()
		except Exception as e:
			obj3=People.objects.get(peopleid=s)
			entry=Review_place_status(review_id=obj1,userid=obj3,helpful=True,report='none')
			entry.save()
		#print (placeid1.place_id)
		return HttpResponse()


def create_reviewStatusReport(request,id=None):
	print("HELLO REPORT")
	if request.method=="POST":
		print("HELLO REPORT1")
		s=4
		if request.session.get("sessionid",None):
			s=request.session['sessionid']
		obj1=Review_place.objects.get(review_id=id)
		print ("Hello ang status")
		report=json.loads(request.body.decode('utf-8'))["report"]
		#Report=Request.POST['report']
		#placeid1=obj1.placeid
		try:
			obj2=Review_place_status.objects.get(review_id=id,userid=s)
			obj2.report=report
			obj2.save()
		except Exception as e:
			obj3=People.objects.get(peopleid=s)
			entry=Review_place_status(review_id=obj1,userid=obj3,helpful=False,report=report)
			entry.save()
			entry1=Admin_notification(category='Report',notification='Reported '+str(report)+' by '+str(s)+' for reviewid '+str(id))
			entry1.save()
		#print (placeid1.place_id)
		return HttpResponse()
	else:
		print("HELLO REPORT2")

		
def load_review(request,id=None):
	#if request.method=='POST':
	s=9
	if request.session.get("sessionid",None):
		s=request.session['sessionid']
		print(s)
		print("sadsad")

	placeid=id
	review_obj=Review_place.objects.filter(placeid=id).order_by('-review_id')
	review_context_list=[]
	if review_obj:
		for review in review_obj:
				#print(review)
			reviewid=review.review_id
			reviewtxt=review.review_text
			d=review.dateandtime
				#placeid=review.placeid
			userid=review.userid
			user_obj=People.objects.get(peopleid=str(userid))
			#review_status_obj_helpful=Review_place_status.objects.filter(review_id=,userid=user_obj)

				#review_status_obj_unlike=Review_place_status.objects.filter(review_id=reviewid,userid=sessionid)
			count_review_helpful=len(Review_place_status.objects.filter(review_id=reviewid,helpful=True))
				#count_review_unlike=len(Review_place_status.objects.filter(review_id=reviewid,review_status="unlike"))
				#if review_status_obj:
				#reviewstatus=review_status_obj.review_status
				#elif not review_status_obj
			#reviewstatus=''
			#obj1=People.objects.get(peopleid=s)
			#obj3=People.objects.get(peopleid=userid)
			#obj2=Review_place.objects.filter(placeid=id,userid=userid)
			try:

				review_status_obj=Review_place_status.objects.get(review_id=reviewid,userid=s)
			except Exception as e:
				review_status_obj=Review_place_status
				review_status_obj.helpful=False
				review_status_obj.report=None
			print(review_status_obj)
			if user_obj:
				username=user_obj.username
				pic=user_obj.photo
				#print(username)
				reviewuserid=user_obj.peopleid
			review_context={}
			review_context['dateandtime']=d
			review_context['reviewid']=reviewid
			review_context['reviewtxt']=reviewtxt
			review_context['userid']=reviewuserid
			review_context['pic']=pic
			review_context['username']=username
			review_context['helpful']=review_status_obj.helpful
			review_context['noofhelpful']=count_review_helpful
			review_context['irrelevant']=1
			review_context['abusive']=2
			review_context['hateful']=3
			review_context_list.append(review_context)
	#print("hello")
	return JsonResponse(review_context_list,safe=False)


def search_in_waston(list_of_key,obj):
	result_list=[]
	for key in list_of_key:
		result=watson.filter(obj,key)
		if result:
			result_list.append(result)
			print("helloma")
	#print(result_list)		
	return result_list

def create_follow_people(request):
	if request.method == "POST":
		if request.session.get("sessionid",None):
			sessionid=request.session["sessionid"]
			viewuserid = search_text=json.loads(request.body.decode('utf-8'))['userid']
			people_obj = People.objects.get(peopleid=sessionid)
			try:
				
				other_people_obj = people_obj.manytomanypeopleid.get(peopleid=viewuserid)
				people_obj.manytomanypeopleid.remove(other_people_obj)
				status_follow = False
			except Exception as e:
				print (str(e))
				people_obj.manytomanypeopleid.add(viewuserid)
				status_follow = True

			all_follow_people_obj = people_obj.manytomanypeopleid.all()
			count_followers = len(all_follow_people_obj)

			return JsonResponse({'nooffollowers': count_followers, 'status': status_follow}, safe=False)

def create_follow_place(request):
	if request.method == "POST":
		
		# sessionid=request.session.get("sessionid")
		# placeid=id
		if request.session.get("sessionid",None):
			sessionid=request.session["sessionid"]
			placeid = json.loads(request.body.decode('utf-8'))['placeid']
			placetype = str(json.loads(request.body.decode('utf-8'))['type'])

			people_obj = People.objects.get(peopleid=sessionid)

			try:
				place_type_obj = people_obj.manytomanyplacetype.get(placetype=placetype,place=placeid)
				people_obj.manytomanyplacetype.remove(place_type_obj)
				#place_type_obj.delete()
				statusplacefollow = False
			except Exception as e:
				try:
					place_type_obj=PlaceType.objects.get(placetype=placetype,place=Place(placeid))
				except Exception as e:
					place_type_obj=PlaceType(placetype=placetype,place=Place(placeid)).save()
					place_type_obj=PlaceType.objects.get(placetype=placetype,place=Place(placeid))
				people_obj.manytomanyplacetype.add(place_type_obj)
				statusplacefollow = True

			try:
				#placefollowers=people_obj.manytomanyplacetype.filter(placetype=placetype,place=Place(placeid)).count()
				placefollowers=People.objects.filter(manytomanyplacetype__placetype=placetype,manytomanyplacetype__place=Place(placeid)).count()
				
				#place_follow_obj = people_obj.manytomanyplaceid.all()
				#count_place_follow = len(place_follow_obj)

			except Exception as e:
				placefollowers = 0
				print(e)

			return JsonResponse({'status': statusplacefollow, 'placefollowers': placefollowers,'type':placetype},safe=False)



def placesearch(request):
	placename=reviewtxt=json.loads(request.body.decode('utf-8'))["placename"]
	place_list=[]
	print(placename)
	place_list_obj=Place.objects.filter(title__istartswith=placename);
	for place in place_list_obj:
		temp={}
		temp["title"]=place.title
		temp["id"]=place.place_id
		place_list.append(temp)
	print(place_list)
	return JsonResponse(place_list,safe=False)

def hobbysearch(request):
	hobbytagname=reviewtxt=json.loads(request.body.decode('utf-8'))["hobbytagname"]
	hobby_list=[]
	hobby_list_obj=search_model.hobbytag.objects.filter(name__istartswith=hobbytagname);
	for hobbytag in hobby_list_obj:
		temp={}
		temp["title"]=hobbytag.name
		hobby_list.append(temp)
	print(hobby_list)
	return JsonResponse(hobby_list,safe=False)



#cr function


def count_credibility_function(request):
	userid=json.loads(request.body.decode('utf-8'))["userid"] 
	return credibility_function(userid,request)



def credibility_function(userid,request):
	if request.method == "POST":
		print("hello")
		tippoint = 9
		articlepoint = 11
		questionpoint = 7
		answerpoint = 7
		placereviewpoint = 6
		photopostpoint = 5
		trippoint = 5

		ultimatetag = 1
		hobbytag = 3
		regiontag = 5
		locationtag = 9
		ltcounttip=0
		htcounttip=0
		utcounttip=0
		rtcounttip=0
		ltcounttrip = 0
		rtcounttrip = 0
		htcounttrip = 0
		utcounttrip = 0
		ltcountphoto = 0
		rtcountphoto = 0
		htcountphoto = 0
		utcountphoto = 0
		ltcountarticle = 0
		rtcountarticle = 0
		htcountarticle = 0
		utcountarticle = 0
		count_article_superlike_points=0
		count_article_like_points=0
		count_trip_superlike_points=0
		count_trip_like_points=0
		count_article_report=0
		count_trip_report=0


		count_photo_report=0

		# first credibility phase


		try:
			tipobj = People_Tips.objects.filter(tipuserid=userid)
			for tips in tipobj:
				if tips.placeid != '':
					ltcounttip = ltcounttip + 1
				elif tips.locationtag == ''  and tips.hobbytag != '':
					htcounttip = htcounttip + 1
				elif tips.locationtag == ''  and tips.hobbytag == '':
					utcounttip = utcounttip + 1

		except Exception as e:
			ltcounttip = 0
			rtcounttip = 0
			htcounttip = 0
			utcounttip = 0

		totaltippoint = ltcounttip * (tippoint + locationtag) + rtcounttip * (
			tippoint + regiontag) + htcounttip * (tippoint + hobbytag) + utcounttip * (tippoint + ultimatetag)

		try:
			tripobj = People_Trips.objects.filter(userid=userid)
			for trips in tripobj:
				if trips.placeid != '':
					ltcounttrip = ltcounttrip + 1
				
				elif trips.locationtag == ''  and trips.hobbytag != '':
					htcounttrip = htcounttrip + 1
				elif trips.locationtag == ''  and trips.hobbytag == '':
					utcounttrip = utcounttrip + 1

		except Exception as e:
			ltcounttrip = 0
			rtcounttrip = 0
			htcounttrip = 0
			utcounttrip = 0

		totaltrippoint = ltcounttrip * (trippoint + locationtag) + rtcounttrip * (
			trippoint + regiontag) + htcounttrip * (trippoint + hobbytag) + utcounttrip * (
			trippoint + ultimatetag)

		try:
			photoobj = People_Photo_Post.objects.filter(userid=userid)
			for photos in photoobj:
				if photos.placeid != '':
					ltcountphoto = ltcountphoto + 1
				elif photos.locationtag == ''  and photos.hobbytag != '':
					htcountphoto = htcountphoto + 1
				elif photos.locationtag == ''  and photos.hobbytag == '':
					utcountphoto = utcountphoto + 1

		except Exception as e:
			ltcountphoto = 0
			rtcountphoto = 0
			htcountphoto = 0
			utcountphoto = 0

		totalphotopostpoint = ltcountphoto * (photopostpoint + locationtag) + rtcountphoto * (
			photopostpoint + regiontag) + htcountphoto * (photopostpoint + hobbytag) + utcountphoto * (
			photopostpoint + ultimatetag)

		try:
			articleobj = People_Article.objects.filter(userid=userid)
			for articles in articleobj:
				if articles.placeid != '':
					ltcountarticle = ltcountarticle + 1
			  
				elif articles.placesid == ''  and list(articles.hobbytags.all()) != '':
					htcountarticle = htcountarticle + 1
				elif articles.locationtag == ''  and articles.hobbytag == '':
					utcountarticle = utcountarticle + 1

		except Exception as e:
			ltcountarticle = 0
			rtcountarticle = 0
			htcountarticle = 0
			utcountarticle = 0

		totalarticlepoint = ltcountarticle * (articlepoint + locationtag) + rtcountarticle * (
			articlepoint + regiontag) + htcountarticle * (articlepoint + hobbytag) + utcountarticle * (
			articlepoint + ultimatetag)

		try:
			questionobj = People_Question.objects.filter(userid=userid)
			countquestions = len(questionobj)
		except Exception as e:
			countquestions = 0

		totalquestionpoint = countquestions * questionpoint

		try:
			answerobj = People_Answer.objects.filter(userid=userid)
			countanswers = len(answerobj)
		except Exception as e:
			countanswers = 0

		totalanswerpoint = countanswers * answerpoint

		try:
			reviewobj = Review_Place.objects.filter(userid=userid)
			countreviews = len(reviewobj)
		except Exception as e:
			countreviews = 0

		totalreviewpoint = countreviews * placereviewpoint

		firstcredibilitypoints = totaltippoint + totaltrippoint + totalarticlepoint + totalphotopostpoint + totalquestionpoint + totalanswerpoint + totalreviewpoint

		#second credibiltity starts

		followerpoint = 6
		superlikearticlepoint = 5
		superlikephotopostpoint = 4
		superliketrippoint = 4
		helpfultippoint = 4
		likearticlepoint = 3
		likephotopostpoint = 3
		liketrippoint = 3

		questionhelpfulpoint = 3
		answerhelpfulpoint = 3
		reviewhelpfulpoint = 2

		try:
			people_obj = People.objects.get(peopleid=userid)
			follow_obj = people_obj.manytomanypeopleid.all()
			for followers in follow_obj:
				followeruserid = followers.peopleid
				people_obj = People.objects.get(peopleid=str(followeruserid))
				credibilitypoints = people_obj.credibilitypoint
				if credibilitypoints >= 0 and credibilitypoints < 100:
					weight = 1
					countsmfollow = countsmfollow + 1
				elif credibilitypoints >= 100 and credibilitypoints < 500:
					weight = 3
					countmdfollow = countmdfollow + 1
				elif credibilitypoints >= 500:
					weight = 7
					countlgfollow = countlgfollow + 1

				count_follow_points = countsmfollow * 1 + countmdfollow * 3 + countlgfollow * 7


		except Exception as e:
			count_follow_points = 0

		try:
			# people_obj = People.objects.get(peopleid=userid)
			#article_obj = People_Article.objects.filter(userid=userid)
			people_obj = People.objects.get(peopleid=userid)

			article_obj = people_obj.manytomanyarticlestatusid.all()
			for articles in article_obj:
				articleuserid = articles.userid
				credibilitypoints=articleuserid.credibilitypoint

				reportstatus = article.report


				if articles.status=='superlike':


					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmsuperlike = countsmsuperlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdsuperlike = countmdsuperlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlgsuperlike = countlgsuperlike + 1

				if articles.status=='like':

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1
					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1

				if reportstatus == 'content irrelevant':
					articleirrevant = articleirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					articleabusive = articleabusive + 1
				elif reportstatus == 'Hateful Content':
					articlehateful = articlehateful + 1
				elif reportstatus == 'none':
					articlenone = articlenone + 1

				else:
					articleother = articleother + 1

				count_article_report = articleirrevant * 11 + articleother * 11 + articleabusive * 25 + articlehateful * 20 + articlenone * 0

				count_article_like_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7
				count_article_superlike_points=countsmsuperlike*1 + countmdsuperlike*3 + countlgsuperlike*7

		except Exception as e:

			count_article_superlike_points=0
			count_article_like_points=0
			count_article_report=0


			# count_article_superlike=len(article_superlike_obj)
		print(count_article_superlike_points)
		try:
			# people_obj = People.objects.get(peopleid=userid)
			#article_obj = People_Article.objects.filter(userid=userid)
			people_obj = People.objects.get(peopleid=userid)

			photopost_obj = people_obj.manytomanyphotopoststatusid.all()
			for photoposts in photopost_obj:
				photopostuserid = photoposts.userid
				credibilitypoints = photopostuserid.credibilitypoint
				reportstatus = photo.report
				print("helloxyz")
				print(photoposts.status)
				if photoposts.status == 'superlike':

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmsuperlike = countsmsuperlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdsuperlike = countmdsuperlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlgsuperlike = countlgsuperlike + 1

				if photoposts.status == 'like':

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1
					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1

				if reportstatus == 'content irrelevant':
					photoirrevant = photoirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					photoabusive = photoabusive + 1
				elif reportstatus == 'Hateful Content':
					photohateful = photohateful + 1
				elif reportstatus == 'none':
					photonone = photonone + 1

				else:
					photoother = photoother + 1

				count_photo_report = photoirrevant * 11 + photoother * 11 + photoabusive * 25 + photohateful * 20 + photonone * 0

				count_photopost_like_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7
				count_photopost_superlike_points=countsmsuperlike*1+countmdsuperlike*3 + countlgsuperlike*7
		except Exception as e:

			count_photopost_superlike_points = 0
			count_photopost_like_points = 0
			count_photo_report=0

		try:
			# people_obj = People.objects.get(peopleid=userid)
			#trip_obj = People_.objects.filter(userid=userid)
			people_obj = People.objects.get(peopleid=userid)

			trip_obj = people_obj.manytomanytripstatusid.all()
			for trips in trip_obj:
				tripuserid = trips.userid
				credibilitypoints = tripuserid.credibilitypoint

				reportstatus = trips.report

				if trips.status == 'superlike':

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmsuperlike = countsmsuperlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdsuperlike = countmdsuperlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlgsuperlike = countlgsuperlike + 1

				if trips.status == 'like':

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1
					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1

				if reportstatus == 'content irrelevant':
					tripirrevant = tripirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					tripabusive = tripabusive + 1
				elif reportstatus == 'Hateful Content':
					triphateful = triphateful + 1
				elif reportstatus == 'none':
					tripnone = tripnone + 1

				else:
					tripother = tripother + 1

				count_trip_report = tripirrevant * 11 + tripother * 11 + tripabusive * 25 + triphateful * 20 + tripnone * 0

				count_trip_like_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7
				count_trip_superlike_points = countsmsuperlike * 1 + countmdsuperlike * 3 + countlgsuperlike * 7
		except Exception as e:

			count_trip_superlike_points = 0
			count_trip_like_points = 0
			count_trip_report=0


		try:
			people_obj = People.objects.get(peopleid=userid)

			tip_obj = people_obj.manytomanytipstatusid.all()
			for tips in tip_obj:
				tipuserid = tips.userid
				credibilitypoints = tipuserid.credibilitypoint
				reportstatus = tips.report

				if tips.status == True:

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1

				if reportstatus == 'content irrelevant':
					tipirrevant = tipirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					tipabusive = tipabusive + 1
				elif reportstatus == 'Hateful Content':
					tiphateful = tiphateful + 1
				elif reportstatus == 'none':
					tipnone = tipnone + 1

				else:
					tipother = tipother + 1

			count_tip_report = tipirrevant * 11 + tipother * 11 + tipabusive * 25 + tiphateful * 20 + tipnone * 0

			count_tip_helpful_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7

		except Exception as e:
			count_tip_helpful_points=0
			count_tip_report=0

		try:
			people_obj = People.objects.get(peopleid=userid)

			question_obj = people_obj.manytomanyquestionstatusid.all()
			for questions in question_obj:
				questionuserid = questions.userid
				credibilitypoints = questionuserid.credibilitypoint
				reportstatus = questions.report

				if questions.status == True:

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1


				if reportstatus == 'content irrelevant':
					questionirrevant = questionirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					questionabusive = questionabusive + 1
				elif reportstatus == 'Hateful Content':
					questionhateful = questionhateful + 1
				elif reportstatus == 'none':
					questionnone = questionnone + 1

				else:
					questionother = questionother + 1

			count_question_report = questionirrevant * 11 + questionother * 11 + questionabusive * 25 + questionhateful * 20 + questionnone * 0

			count_question_helpful_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7

		except Exception as e:
			count_question_helpful_points = 0
			count_question_report=0

		try:
			people_obj = People.objects.get(peopleid=userid)

			answer_obj = people_obj.manytomanyanswerstatusid.all()
			for answers in answer_obj:
				answeruserid = answers.userid
				credibilitypoints = answeruserid.credibilitypoint
				reportstatus = answers.report
				if answers.status == True:

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1


				if reportstatus == 'content irrelevant':
					answerirrevant = answerirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					answerabusive = answerabusive + 1
				elif reportstatus == 'Hateful Content':
					answerhateful = answerhateful + 1
				elif reportstatus == 'none':
					answernone = answernone + 1

				else:
					answerother = answerother + 1

			count_answer_report = answerirrevant * 11 + answerother * 11 + answerabusive * 25 + answerhateful * 20 + answernone * 0

			count_answer_helpful_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7

		except Exception as e:
			count_answer_helpful_points = 0
			count_answer_report=0


		try:
			people_obj = People.objects.get(peopleid=userid)

			review_obj = people_obj.manytomanyreviewstatusid.all()
			for reviews in review_obj:
				reviewuserid = reviews.userid
				credibilitypoints = reviewuserid.credibilitypoint
				reportstatus = reviews.report

				if reviews.status == True:

					if credibilitypoints >= 0 and credibilitypoints < 100:
						weight = 1
						countsmlike = countsmlike + 1

					elif credibilitypoints >= 100 and credibilitypoints < 500:
						weight = 3
						countmdlike = countmdlike + 1
					elif credibilitypoints >= 500:
						weight = 7
						countlglike = countlglike + 1


				if reportstatus == 'content irrelevant':
					reviewirrevant = reviewirrevant + 1
				elif reportstatus == 'Abusive and Explicit Content':
					reviewabusive = reviewabusive + 1
				elif reportstatus == 'Hateful Content':
					reviewhateful = reviewhateful + 1
				elif reportstatus == 'none':
					reviewnone = reviewnone + 1

				else:
					reviewother = reviewother + 1

			count_review_report = reviewirrevant * 11 + reviewother * 11 + reviewabusive * 25 + reviewhateful * 20 + reviewnone * 0

			count_review_points = countsmlike * 1 + countmdlike * 3 + countlglike * 7

		except Exception as e:
			count_review_points = 0
			count_review_report=0



		secondcredibilitypoints = count_follow_points * followerpoint + count_article_superlike_points * superlikearticlepoint + count_article_like_points * likearticlepoint + count_trip_superlike_points * superliketrippoint + count_trip_like_points * liketrippoint + count_photopost_superlike_points * superlikephotopostpoint + count_photopost_like_points * likephotopostpoint + count_tip_helpful_points * helpfultippoint + count_question_helpful_points * questionhelpfulpoint + count_answer_helpful_points * answerhelpfulpoint + count_review_points * reviewhelpfulpoint

		# Third Credibility Starts

		thirdcredibilitypoints=count_article_report+count_trip_report+count_photo_report+count_tip_report+count_question_report+count_answer_report+count_review_report


		totalcredibilitypoints=firstcredibilitypoints+secondcredibilitypoints-thirdcredibilitypoints
		print(totalcredibilitypoints)
		user_obj=People.objects.get(peopleid=userid)
		user_obj.point=str(totalcredibilitypoints+int(user_obj.adminpoint))
		user_obj.save()

		print("userpoint")
		print(user_obj.username)
		print(user_obj.point)

		return JsonResponse({'credibilitypoint':totalcredibilitypoints+int(user_obj.adminpoint)},safe=False)

def adminloginview(request):
	return render(request,"posts/adminlogin.html")
