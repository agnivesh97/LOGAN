from django.shortcuts import render
from .models import *
from django.core.serializers import json
import json
from django.http import JsonResponse
#from urllib.parse import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
import posts
from posts.models import *
from collections import OrderedDict
# Create your views here.
def temp_update(request):
	try:
		id=request.GET.get('placeid')
		text=request.GET.get('text')
		textid=request.GET.get('textid')
		userid=request.session.get('sessionid',1)
		peo=People.objects.get(peopleid=userid)
		pla=Place.objects.get(place_id=id)
		try :
			instance=Place_temp.objects.get(place_id=pla,user_id=peo)
		except Exception as e: 
			instance=Place_temp(place_id=pla,user_id=peo)
			instance.save()
		if textid == "About This Place":
			instance.about_the_trek=text
		elif textid == "Highest Altitude":
			instance.highest_altitude=text
		elif textid == 'Location':
			instance.state=text
		elif textid == 'Wildlife Reserve':
			instance.wildlife_reserve=text

		elif textid == 'Best Time':
			instance.best_time=text

		elif textid == 'What To Explore':
			i=0

		elif textid == "Food":
			i=0
		elif textid == "Accomodations":
			instance.accomodation=text

		elif textid == 'Fitness':
			i=0
		elif textid == 'Equipments':
			i=0
		elif textid == "Trail Route":
			instance.trek_route=text
		elif textid == "Trail Highlights":
			instance.trail_highlights=text

		elif textid == "Onwards":
			i=0
		elif textid == 'Route Details':
			i=0
		elif textid == "Police Station":
			instance.police_station=text
		elif textid == "ATM":
			instance.atm=text
		elif textid =="Airport":
			instance.airport=text
		elif textid == "BusStation":
			instance.bus_stand=text
		elif textid == "Best Time to Visit":
			instance.best_time=text
		elif textid == "Open Timings":
			instance.open_timings=text
		elif textid == "Weather Details":
			instance.weather_details=text
		elif textid == "Govt. Guidelines":
			instance.govt_guidelines=text
		elif textid == "Languages Spoken":
			instance.languages_spoken=text
		elif textid == "Commonly Visited From":
			instance.commonly_visited_from=text
		elif textid == "Popular Route":
			instance.popular_route=text
		instance.save()
		data={}
		data['is_taken']=True
		return JsonResponse(data);
	except Exception as e:
		data={}
		data['is_taken']=False
		return JsonResponse(data);

def addplace(request):
	placeinfo = json.loads(request.body.decode('utf-8'))["placeinfo"]
	print(placeinfo)
	user_obj=People.objects.get(peopleid=placeinfo["user_id"])
	new_place_obj=New_place(user_id=user_obj,data=placeinfo)
	new_place_obj.save()
	#print(placeinfo)

	return JsonResponse(True,safe=False)

def showlist(request):
	try:
		adminuser=request.POST["username"]
		adminpass=request.POST["password"]
		if not request.session.get("adminlogin",None):
			login=Adminlogin.objects.get(username=adminuser,password=adminpass)
			request.session["adminlogin"]=login.id
		place_edit=Place_temp.objects.all()
		infolist=[]
		print(place_edit)
		for place_edit_obj in place_edit:
			placename=(place_edit_obj.place_id).title
			username=(place_edit_obj.user_id).username
			info={}
			info["user_id"]=(place_edit_obj.user_id).peopleid
			info["username"]=username
			info["place_id"]=(place_edit_obj.place_id).place_id
			info["placename"]=placename
			infolist.append(info)
		return render(request,"posts/placeedit.html",{"place_edit":infolist})
	except Exception as e:
		print(e)
		return redirect("/adminlogin/")

def showedit(request,place_id=None,user_id=None):
	if not request.session.get('sessionid',None):
		#messages.info(request,'Login Required')
		return HttpResponseRedirect('/')
	instance = Place_temp.objects.get(place_id=place_id,user_id=user_id)
	#share_string = quote_plus(instance.title)
	status=False
	status1=False
	status2=False
	user_obj=None
	places_visited=0
	places_wished=0
	places_follow=0
	follower=0
	sessionid=request.session["sessionid"]

	#print("gadbad statussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
	#print (status2)
	#share_string = quote_plus(instance.title)
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
		
		"instance" : Place.objects.get(title=instance.place_id),
		"gernal_info" : gernal_info,
		"food" : tips,
		"food1" : tips1,
		"trails" :trails,
		"basecampe":basecampe,
		"emergency_locations":emergency_locations,
		"placeid":Place(instance.place_id).place_id,
		"sessionid":sessionid,
		"status":status,
		"status1":status1,
		"status2":status2,
		"tag_list":"",
		"placefollowers":0,
		"placebeenher":0,
		"placerecommended":0,
		"username":username,
		"loginForm":"",
		"registerForm":"",
		"places_visited":places_visited,
		"places_wished":places_wished,
		"places_follow":places_follow,
		"follower":follower,
		"place_id":place_id,
		"user_id":user_id,
		"admin":True,
		"pic":request.session['sessionpic']
	}
	return render(request, "posts/postdetails.html", context)



	