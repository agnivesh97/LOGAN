from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from edite_data.models import *
from django.core.serializers import json
import json
from watson import search as watson
import time
from watson import search as watson

from geosimple import*

from geopy.distance import Distance
import social_network

from social_network import views as vi


distance_m = 200000
origin = (18.516726,73.856255)

#closest_spot = Spot.objects.filter(point__distance_lte=(origin, D(m=distance_m))).distance(origin).order_by('distance')[:1][0]

otherwords=["on","in","and","or","near","at","from"]
return_list=[]
# Create your views here.
def search(request):
	global return_list,origin
	#print(request.session["location"])
	if request.session.get('location',None):
		origin = (float((request.session["location"])[0]),float((request.session["location"])[0]))
		print("user location")
		print(origin)
	if return_list:
		 del return_list[:] 
	list_of_key=[]
	search_text=json.loads(request.body.decode('utf-8'))['text']
	#data = request.GET
	#search_text = data.get("term")
	print(search_text)
	list_of_key=search_text.split(" ")
	features_obj_list=features.objects.filter(name__icontains=list_of_key[0])
	if features_obj_list:
		return features_search(search_text,features_obj_list)
	hobby_obj_list = search_in_waston(list_of_key,hobbytag)
	if hobby_obj_list:
		#print("hello")
		return hobby_search(search_text,hobby_obj_list)
	else:
		states_obj = watson.filter(states, search_text).first()
		temp={}
		temp["title"]=str(states_obj)
		temp["id"]=5
		return_list.append(temp)
		hobby_obj_list=hobbytag.objects.filter(statename__city=str(states_obj))
		print(hobby_obj_list)
		if hobby_obj_list:
			return hobby_search(search_text,hobby_obj_list,str(states_obj))
		else:
			return HttpResponse(JsonResponse({"places":place_search(" ",search_text)}))


def search_in_waston(list_of_key,obj):
	for key in list_of_key:
		result=watson.filter(obj,key)
		if result:
			return result
	return None



def features_search(search_text,features_obj_list):
	global return_list
	return_list2=[]
	list_of_key=search_text.split(" ")
	for features_obj in features_obj_list:	
		return_list2=place_search(features_obj.name,search_text)	
	return HttpResponse(JsonResponse({"places":return_list}))


def hobby_search(search_text,hobby_obj_list,flage=""):
	global return_list,origin
	list_of_key=search_text.split(" ")
	
	for hobby_obj in hobby_obj_list:
		if flage:

			query=hobby_obj.states(statename).filter(city=flage)
		else:
			query1=list(hobby_obj.statename.all().values("city"))
			queryr1=[d['city'] for d in query1]
			#print(queryr1)
			query=states.objectss.filter(city__in=queryr1,location__distance_lt=(origin,Distance(miles=20000))).order_by_distance()
			
		if len(list_of_key)==1 or flage:
			for states_obj in query:
					temp={}
					temp["title"]=hobby_obj.name+" in "+states_obj.city
					temp["url"]="/logan/?q="+temp["title"]
					return_list.append(temp)
		else :
			for hobby_obj in hobby_obj_list:
				states_obj_list=search_in_waston(list_of_key,hobby_obj.statename)
				#print(states_obj_list)
				if states_obj_list:
					for states_obj in states_obj_list:
						temp={}
						temp["title"]=hobby_obj.name+" in "+states_obj.city
						temp["url"]="/logan/?q="+temp["title"]
						return_list.append(temp)
				else:
					place_search(hobby_obj.name+"in",search_text)
				

	return HttpResponse(JsonResponse({"places":return_list}))


def place_search(prifixword,search_text):
	global return_list
	list_of_key=search_text.split(" ")
	search_results =search_in_waston(list_of_key,Place)
	if search_results:
		if prifixword != " ":
			prifixword=prifixword+" "+"on"
		for place in search_results:
			temp={}
			temp["title"]=prifixword+" "+place.title
			temp["url"]="/place/"+place.title
			return_list.append(temp)
	else:
		search_results =search_in_waston(list_of_key,People)
		if search_results:
			for person in search_results:
				temp={}
				temp["title"]=person.username
				temp["url"]="nothing"
				return_list.append(temp)

	return return_list
	


def loadphotos(request):
	placeid=json.loads(request.body.decode('utf-8'))['placeid']
	place_obj=Place.objects.get(place_id=placeid)
	photos_list=[]
	photo_obj_list=place_obj.people_photo_post_set.all()
	sessionid=request.session.get("sessionid",None)
	for photo_obj in photo_obj_list:
		photos_list.append(vi.load_photo(photo_obj,sessionid))
	print(photos_list)
	return JsonResponse(photos_list,safe=False)









