from django.core.serializers import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
import time
import json
import posts
from posts.models import *
from django.http import HttpResponse
from django.conf import settings
#from django.shortcuts import render_to_response
from os.path import isfile, join
from mimetypes import MimeTypes
from os import listdir

#import wand.image
#from wand.image import Image
import hashlib
import json
import time
import hmac
import copy
import sys
import os

from io import BytesIO
import urllib.request
from urllib.request import urlopen
from django.core.files import File
from django.core.files.base import ContentFile
import requests as rq
from django.core.files.temp import NamedTemporaryFile
import search_app
from search_app import models as search_model
#import urlparse
from html.parser import HTMLParser
from django.core.files.storage import FileSystemStorage
import base64
list1=[]
list2=[]
placeidg=None
hobbytagname=None
global_sessionid=None
placeidarry=[]

class MyParse(HTMLParser):
		def handle_starttag(self, tag, attrs):
				global list1,list2
				if tag=="img":
						i=0
						#print("fhghjgjhgjhgjhgjhghj")
						r=dict(attrs)["src"]
						#r = rq.get(dict(attrs)["src"])
						#print(r)
						
						
							
						img_temp = NamedTemporaryFile()
						img_temp.write(base64.b64decode(r.split(",")[1]))
						 
							#img_temp.write(r.content)
						 #img_temp.write(r.content)
						 #img_temp.flush()
						userid = global_sessionid
						placeid = 7
						fs = FileSystemStorage()
						filename = fs.save("image1.jpg",img_temp)
						photo = Photos(photo=filename, userid=People(userid), placeid=Place(placeid))
						photo.save()
						list1.append(dict(attrs)["src"])
						stri="/media/"+str(photo.photo)+"/"
						list2.append(stri)
						#print(list2)

							 


class LoadMyParse(HTMLParser):
		def handle_starttag(self, tag, attrs):
				global list1,list2
				if tag=="img":
						list2.append(dict(attrs)["src"])


def upload_image(request):

	global placeidg,hobbytagname,global_sessionid
	if request.method == "POST":
		if request.session.get("sessionid",None):
			sessionid=request.session['sessionid']
			pic=request.session['sessionpic']
			articletext = request.POST.get("articlepostcontent")
			articletitle = request.POST.get("articletitle")
			
			hobbytagname = request.POST.get("hobbytagname")
			placename=request.POST.get("placename")
			print(placename)
			print(hobbytagname)
			placeidg = Place.objects.get(title=placename).place_id
			hobbytagnamelist=hobbytagname.split(",")
			#print(articletitle)
			#hobbytag_obj=search_model.hobbytag.objects.get(name=hobbytagname)
			global_sessionid=sessionid
			h = MyParse()
			page = articletext
			h.feed(page)			
			counter=0
			for li in list1:
				page=page.replace(li,list2[counter])
				counter=counter+1
			ratings = 1
			articletime=time.time()
			obj = People_Article(
							articletext=page,
							placeid=Place(placeidg),
							userid=People(sessionid),
							ratings=ratings,
							time=articletime,
							article_title=articletitle)
			obj.save()
			join_t=Join_table(post_article=obj,time=articletime)
			join_t.save()
			for hobbytagname in hobbytagnamelist:
				hobbytag_obj=search_model.hobbytag.objects.get(name=hobbytagname)
				obj.hobbytags.add(hobbytag_obj)
			return(JsonResponse(load_article(obj),safe=False))
	#print("sssasgame")
	return HttpResponse(" ")



def profilehtml(request,id=None):
		if request.session.get("sessionid",None):
			sessionid=request.session['sessionid']
			pic=request.session['sessionpic']
			userinfo=People.objects.get(peopleid=sessionid)
			#user info
			follower=userinfo.manytomanypeopleid.all().count()
			places_visited=userinfo.manytomanyplacetype.filter(placetype=1).count()
			places_wished=userinfo.manytomanyplacetype.filter(placetype=2).count()
			places_follow=userinfo.manytomanyplacetype.filter(placetype=0).count()
			
			
			return render(request, "myprofile.html", {'sessionid':sessionid,'pic':pic,'username':userinfo.username,'follower':follower,'aboutme':userinfo.aboutme,'places_visited':places_visited,'places_wished': places_wished,'places_follow': places_follow})
		return HttpResponse("")

def postarticlepagehtml(request):
	if request.session.get("sessionid",None):
		sessionid=request.session['sessionid']
		pic=request.session['sessionpic']
		return render(request, "article.html", {'sessionid':sessionid,'pic':pic})
	return HttpResponse("")

def create_photo(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session['sessionid']
				pic=request.session['sessionpic']
				photoposttime=time.time()
				ratings=1
				photoposttext=request.POST.get("photoposttext")
				photofile=request.FILES['file1'].name
				img=request.FILES['file1']
				placeid=request.POST.get("placeid")

				photo_obj=Photos(photo=img,placeid=Place(placeid),userid=People(sessionid))
				photo_obj.save()
				print("The requested parameters are"+str(photoposttext)+" "+str(photofile))
				print(ratings)
				entry_photo_post_obj=People_Photo_Post(placeid=Place(placeid),
													  userid=People(sessionid),
													  time=photoposttime,
													  ratings=ratings,
													  photoposttext=photoposttext
													 )
				entry_photo_post_obj.save()
				#print(entry_photo_post_obj.photosimg.all())
				entry_photo_post_obj.photosimg.add(photo_obj)
				#entry_photo_post_obj.save()
				join_t=Join_table(post_photo=entry_photo_post_obj,time=photoposttime)
				join_t.save()
				return(JsonResponse(load_photo(join_t.post_photo,sessionid=sessionid),safe=False))
					#return HttpResponse()

def delete_photo_post(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				pic=request.session["sessionpic"]
				action={}
				photoid=json.loads(request.body.decode("utf-8"))["photoid"]
				try:
						photo_post_obj=People_Photo_Post.objects.get(photopostid=photoid,userid=sessionid)
						photo_post_obj.photosimg.all().delete()
						photo_post_obj.delete()
						action["action"]=True
				except Exception as e:
					print(e)
					action['action']=False

				return JsonResponse(action,safe=False)

def edit_photo_post(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				pic=request.session['sessionpic']
				placeid=json.loads(request.body.decode('utf-8'))["placeid"]
				photoid=json.loads(request.body.decode("utf-8"))["photoid"]
				photoposttext=json.loads(request.body.decode("utf-8"))["photoposttext"]
				try:
						update_photo_post_obj=People_Photo_Post.objects.get(photoid=photoid,userid=sessionid)
						update_photo_post_obj.photoposttext=photoposttext
						update_photo_post_obj.save()

				except Exception as e:
						print(e)

				return HttpResponse()

def create_photo_post_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				pic=request.session["sessionpic"]
				photoid=json.loads(request.body.decode("utf-8"))["photoid"]
				photocomment=json.loads(request.body.decode("utf-8"))["comment"]
				try:
						entry_photo_post_comment_obj=People_Photo_Post_Comment(
																				 userid=People(sessionid),
																				 photopostid=People_Photo_Post(photoid),
																				 photocomment=photocomment
																				 )
						entry_photo_post_comment_obj.save()
				except Exception as e:
						print(e)
				count_comments=People_Photo_Post_Comment.objects.filter(photopostid=photoid).count()
				#count_comments=len(new_photo_comment_obj)
				return JsonResponse({'photopostid':photoid,'noofcomments':count_comments,'photocommentid':entry_photo_post_comment_obj.photocommentid})

def edit_photo_post_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session['sessionid']
				pic=request.session['sessionpic']
				photopostcommentid=json.loads(request.body.decode("utf-8"))["photocommentid"]
				photocomment=json.loads(request.body.decode("utf-8"))["photocomment"]
				try:
						update_obj=People_Photo_Post_Comment.objects.get(photocommentid=photopostcommentid,photopostid=photopostid,userid=sessionid)
						update_obj.photocomment=photocomment
						update_obj.save()

				except Exception as e:
					i=0

				return HttpResponse()

def delete_photo_post_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				photopostid = json.loads(request.body.decode("utf-8"))["photoid"]
				photopostcommentid = json.loads(request.body.decode("utf-8"))["photocommentid"]
				try:
						photo_post_comment_obj = People_Photo_Post_Comment.objects.get(photocommentid=photopostcommentid, photopostid=photopostid, userid=sessionid)
						photo_post_comment_obj.delete()
				except Exception as e:
						print ("The exception is"+str(e))
				return HttpResponse()

def load_photo_post_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
					#placeid=id
				photoid=json.loads(request.body.decode("utf-8"))["photoid"]

				try:
						photo_context_list=[]
						photo_comment_obj=People_Photo_Post_Comment.objects.filter(photopostid=photoid)
						for comments in photo_comment_obj:
								#print ("The comment objects are"+str(comments.photopostid)+" "+str(comments.photocommentid)+" "+str(comments.photocomment)+" "+str(comments.userid))
								photoid=str(comments.photopostid)
								photocommentid=comments.photocommentid
								commentuserid=comments.userid
								commenttext=comments.photocomment
								user_obj=commentuserid
								username=user_obj.username
								comment_context={}
								comment_context['photoid']=photoid
								comment_context['photocommentid']=photocommentid
								comment_context['iseditable']=False
								comment_context['commentuserid']=commentuserid.peopleid
								comment_context['commentusername']=username
								comment_context['commenttext']=commenttext
								comment_context['sessionuserid']=sessionid
								comment_context['user_pic']=user_obj.photo
								photo_context_list.append(comment_context)
								print(photo_context_list)

				except Exception as e:
						print ("The exception is"+str(e))

			return JsonResponse(photo_context_list,safe=False)


def create_photo_post_like(request,id=None):
		if request.method=="POST":
			print("halla")
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				photoid=json.loads(request.body.decode("utf-8"))["photoid"]
				try:
					
						photo_post_status_obj=People_Photo_Post_Status.objects.get(userid=sessionid,photopostid=photoid)
						status=photo_post_status_obj.status
						if status=='superlike':
								photo_post_status_obj.status='like'
								photo_post_status_obj.save()
						elif status=='none':
								photo_post_status_obj.status='like'
								photo_post_status_obj.save()
						elif status=='like':
								photo_post_status_obj.delete()

				except Exception as e:
						entry_photo_post_status_obj=People_Photo_Post_Status(userid=People(sessionid),photopostid=People_Photo_Post(photoid),status='like')
						entry_photo_post_status_obj.save()
				try:
					new_photo_post_status=People_Photo_Post_Status.objects.get(userid=sessionid,photopostid=photoid)
					newstatus=new_photo_post_status.status
				except Exception as e:
					newstatus="none"
				photo_post_status_obj_like=People_Photo_Post_Status.objects.filter(photopostid=photoid,status='like')
				count_like=len(photo_post_status_obj_like)
				photo_post_status_obj_superlike=People_Photo_Post_Status.objects.filter(photopostid=photoid,status='superlike')
				count_superlike=len(photo_post_status_obj_superlike)
				context_like={}
				context_like['placeid']=5
				context_like['sessionuserid']=sessionid
				context_like['photopostid']=photoid
				context_like['status']=newstatus
				context_like['nooflikes']=count_like
				context_like['noofsuperlikes']=count_superlike
				return JsonResponse(context_like,safe=False)


def create_photo_post_superlike(request,id=None):
		if request.method=="POST":
			if request.session.get('sessionid',None):
				sessionid=request.session["sessionid"]
				photoid=json.loads(request.body.decode("utf-8"))["photoid"]
				try:
					#sessionid=request.session.get("sessionid")
						photo_post_status_obj=People_Photo_Post_Status.objects.get(photopostid=photoid,userid=sessionid)
						status=photo_post_status_obj.status
						if status=='like':
								photo_post_status_obj.status='superlike'
								photo_post_status_obj.save()
						elif status=='none':
								photo_post_status_obj.status='superlike'
								photo_post_status_obj.save()
						elif status=='superlike':
								photo_post_status_obj.delete()

				except Exception as e:

						entry_photo_post_status_obj=People_Photo_Post_Status(userid=People(sessionid),photopostid=People_Photo_Post(photoid),status='superlike')
						entry_photo_post_status_obj.save()

				try:
						new_photo_post_status=People_Photo_Post_Status.objects.get(photopostid=photoid,userid=sessionid)
						newstatus=new_photo_post_status.status

				except Exception as e:
						print (e)
						newstatus="none"

				photo_post_status_obj_like=People_Photo_Post_Status.objects.filter(photopostid=photoid,status='like')
				count_like=len(photo_post_status_obj_like)
				photo_post_status_obj_superlike=People_Photo_Post_Status.objects.filter(photopostid=photoid,status='superlike')
				count_superlike=len(photo_post_status_obj_superlike)

				context_superlike={}
				context_superlike['placeid']=5
				context_superlike['sessionuserid']=sessionid
				context_superlike['photopostid']=photoid
				context_superlike['status']=newstatus
				context_superlike['nooflikes']=count_like
				context_superlike['noofsuperlikes']=count_superlike

				return JsonResponse(context_superlike,safe=False)

def create_photo_report(request,id=None):
	if request.method=="POST":
		if request.session.get("sessionid",None):
			sessionid=request.session["sessionid"]
			photoid=json.loads(request.body.decode("utf-8"))["photoid"]
			newphotoreport=json.loads(request.body.decode("utf-8"))["report"]
			print ("The request parameters are"+str(photoid)+str(newphotoreport))
			try:
					photo_status_report_obj=People_Photo_Post_Status.objects.get(userid=sessionid,photopostid=photoid)
					photo_status_report_obj.report=newphotoreport
					photo_status_report_obj.save()
					print("save")
			except Exception as e:
					print(e)
					entry_photo_status_report_obj=People_Photo_Post_Status(userid=People(sessionid),status='none',photopostid=People_Photo_Post(photoid),report=newphotoreport)
					entry_photo_status_report_obj.save()
					return HttpResponse()
			return HttpResponse()

def load_photo_post(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				placeid=id
				typev=json.loads(request.body.decode('utf-8'))["type"] 
				other_userid=json.loads(request.body.decode('utf-8')).get("other_userid",None)
				#return HttpResponse("<script>alert('skasjk'); </script>")
				print(other_userid)
				try:
						if typev=="myphotos" or typev=="photos":
							if other_userid:
								return load_other_photo_post(sessionid=sessionid,id=other_userid)
							return load_my_photo_post(sessionid)
						if typev=="myarticles" or typev=="articles":
							if other_userid:
								return load_otherarticles(sessionid=sessionid,id=other_userid)
							return load_myarticles(sessionid)
						if typev=="mytrips" or typev=="trips":
							if other_userid:
								return load_othertrips(sessionid=sessionid,id=other_userid)
							return load_mytrips(sessionid)
						if typev=="mytips" or typev=="tips":
							if other_userid:
								return load_other_tips(sessionid=sessionid,id=other_userid)
							return load_other_tips(sessionid=sessionid,id=sessionid)
						photo_context_list=[]
						if id == None:
							Join_table_list=Join_table.objects.get(id=id)
						else:
							Join_table_list=Join_table.objects.all().order_by("-time")
						for Join_table_obj in Join_table_list:
								if Join_table_obj.post_photo:
										photo_context_list.append(load_photo(Join_table_obj.post_photo,sessionid=sessionid))
								elif Join_table_obj.post_trips:
										photo_context_list.append(load_t(Join_table_obj.post_trips,sessionid=sessionid))
								elif Join_table_obj.post_article:
										photo_context_list.append(load_article(Join_table_obj.post_article,sessionid=sessionid))
								elif Join_table_obj.post_tip:
										photo_context_list.append(load_tips(Join_table_obj.post_tip,sessionid=sessionid))

						
						#print(photo_context_list)
				except Exception as e:
						print("The exception is "+str(e))
						#print (photo_context_list)
				if id == None:
					return render(request,"showcard.html",photo_context_list[0])
				return JsonResponse(photo_context_list,safe=False)

def share(request):
	if request.session.get("sessionid",None):
		sessionid=request.session['sessionid']
	else:
		sessionid=None
	type_obj=request.GET['type']
	obj_id=request.GET['id']
	if "/" in obj_id:
		obj_id=obj_id[:-1]
	photo_context_list=[]
	if type_obj=='photos':
		photo_obj=People_Photo_Post.objects.get(photopostid=obj_id);
		photo_context_list.append(load_photo(photo_obj,sessionid=sessionid))	
	elif type_obj=='trips':
		trip_obj=People_Trips.objects.get(tripid=obj_id)
		photo_context_list.append(load_t(trip_obj,sessionid=sessionid))

	"""
	elif type_obj='article':
			photo_context_list.append(load_article(Join_table_obj.post_article,sessionid=sessionid))
	
	elif type_obj='post_tip':
			photo_context_list.append(load_tips(Join_table_obj.post_tip,sessionid=sessionid))
	"""
	print(photo_context_list[0])
	if request.GET.get('q',None):
		return JsonResponse({"data":photo_context_list[0],"id":obj_id},safe='false')
	else:
		return render(request,"showcard.html",photo_context_list[0])


def load_article(article_objs,sessionid=None,placeid=5):
		global list2
		del list2[:]
		h = HTMLParser()
		context_article = {}
		articletext=article_objs.articletext
		userid = article_objs.userid
		ratings = article_objs.ratings
		username = userid.username
		pic=userid.photo
		articleid=article_objs.articleid
		placename=article_objs.placeid.title
		hobbytagname_list=list(article_objs.hobbytags.all())
		if hobbytagname_list:
			hobbytagname=hobbytagname_list[0]
			context_article["hobbytagname"]=str(hobbytagname)
		if sessionid:
			try:
					article_like_obj=People_Article_Status.objects.filter(articleid=articleid, status='like')
					nooflike = len(article_like_obj)

			except Exception as e:
					nooflike=0
			try:

					article_superlike_obj=People_Article_Status.objects.filter(articleid=articleid, status='superlike')
					noofsuperlike = len(article_superlike_obj)

			except Exception as e:
					noofsuperlike=0

			try:
					article_comment_obj=People_Article_Comment.objects.filter(articleid=articleid)
					noofcomment=len(article_comment_obj)

			except Exception as e:
					noofcomment=0

			try:
					status_obj = People_Article_Status.objects.get(articleid=articleid, userid=sessionid)
					status = status_obj.status
			except Exception as e:
					status = False
			context_article['ratings'] = ratings
			
			context_article['nooflike'] = nooflike
			context_article['noofsuperlike'] = noofsuperlike
			context_article['noofcomment']=noofcomment
			context_article['status'] = status
			context_article['sessionuserid']=sessionid

		h1 = LoadMyParse()
		page = article_objs.articletext
		h1.feed(page)
		context_article['username'] = username
		context_article['articleid'] = articleid
		context_article['articletext'] = h.unescape(articletext)
		context_article['articletitle']=article_objs.article_title
		context_article['articleuserid'] = userid.peopleid       
		context_article['user_pic']=pic
		context_article['type']="articles"
		if len(list2)>0:
			context_article['img_link']=list2[0]
		context_article['placename']=placename
		return context_article
					



def load_photo(photos,sessionid=None,placeid=5):
		photoid=photos.photopostid
		#print(photos.userid.username)
		userid=photos.userid
		placename=photos.placeid.title
		if not userid.username:
				userid=People.objects.get(peopleid=int(str(photos.userid)))
		photoposttext=photos.photoposttext
		photo_pic=(photos.photosimg.all())[0]
		username=userid.username
		print(username)
		pic=userid.photo
		try:
				photo_status_obj=People_Photo_Post_Status.objects.get(photopostid=photoid,userid=sessionid)
				status=photo_status_obj.status
		except Exception as e:
				print(str(e))
				status='none'

		try:
				photo_status_obj_like=People_Photo_Post_Status.objects.filter(photopostid=photoid,status='like')
				count_likes=len(photo_status_obj_like)
		except Exception as e:
				print (e)
				count_likes=0
		try:
				photo_status_obj_superlike=People_Photo_Post_Status.objects.filter(photopostid=photoid,status='superlike')
				count_superlikes=len(photo_status_obj_superlike)
		except Exception as e:
				print (e)
				count_superlikes=0
		try:
				photo_status_comment_obj=People_Photo_Post_Comment.objects.filter(photopostid=photoid)
				count_comments=len(photo_status_comment_obj)
		except Exception as e:
				print(e)
				count_comments=0

		photo_post_context={}
		photo_post_context['photopostid']=photoid
		photo_post_context['photopostuserid']=userid.peopleid
		photo_post_context['photoposttext']=photoposttext
		photo_post_context['username']=username
		photo_post_context['status']=status
		photo_post_context['sessiouserid']=sessionid
		photo_post_context['nooflikes']=count_likes
		photo_post_context['noofsuperlikes']=count_superlikes
		photo_post_context['noofcomments']=count_comments
		photo_post_context['photo_pic']=str(photo_pic.photo)
		photo_post_context['user_pic']=str(pic)
		photo_post_context['type']="photos"
		photo_post_context['placename']=placename
		print (photo_post_context['user_pic'])
		return photo_post_context
		#photo_context_list.append(photo_post_context)


def load_t(trips,sessionid=None,placeid=5):
		print("hello2")
		tripid=trips.tripid
								#trip_location = trips.trip_location
		travel_starting_date = trips.travel_starting_date
		travel_ending_date = trips.travel_ending_date
		nooftravelerscurrent = trips.nooftravelerscurrent
		nooftravelersrequired = trips.nooftravelersrequired

		trip_plannning = trips.trip_planning
		expenses_details = trips.expenses_details
		preferences=trips.preferences
		phone_no = trips.phone_number
		travelingfrom=trips.traveling_from
		travelingto=trips.traveling_to
		email = trips.email
		userid = trips.userid
		if not userid.username:
				userid=People.objects.get(peopleid=People(userid))
		time = trips.time
		pic=userid.photo
		try:
				trip_status_obj=People_Trips_Status.objects.get(tripid=tripid,userid=sessionid)
				status=trip_status_obj.status

		except Exception as e:
				print("hadha")
				print(e)
				status="None"
		try:
				trip_status_obj_like=People_Trips_Status.objects.filter(tripid=tripid,status='like')
				count_likes=len(trip_status_obj_like)
		except Exception as e:
				print("2")
				count_likes=0

								#user_obj = People.objects.get(peopleid=str(userid))

		try:
				trip_status_obj_superlike=People_Trips_Status.objects.filter(tripid=tripid,status='superlike')
				count_superlikes=len(trip_status_obj_superlike)
		except Exception as e:
				print("3")
				count_superlikes=0

		if userid:
				username=userid.username
				tripuserid=userid.peopleid

		try:
				trip_comment_obj=People_Trips_Comment.objects.filter(tripid=tripid)
				count_comment=len(trip_comment_obj)
		except Exception as e:
				print("3")
				count_comment=0

		trip_context={}
		trip_context['tripusername']=username
		trip_context['tripuserid']=tripuserid
		trip_context['tripid']=tripid
		#trip_context['triplocation']=trip_location
		trip_context['travelingfrom']=travelingfrom
		trip_context['travelingto']=travelingto
		trip_context['tripstartingdate']=travel_starting_date
		trip_context['tripendingdate']=travel_ending_date
		trip_context['noofcurrenttravelers']=nooftravelerscurrent
		trip_context['noofrequiredtravelers']=nooftravelersrequired
		trip_context['prefference']=preferences
		trip_context['tripplanning']=trip_plannning
		trip_context['expensesdetails']=expenses_details
		trip_context['tripphoneno']=phone_no
		trip_context['email']=email
		trip_context['status']=status
		trip_context['nooflikes']=count_likes
		trip_context['noofsuperlikes']=count_superlikes
		trip_context['noofcomments']=count_comment
		trip_context['sessionuserid']=sessionid
		trip_context['user_pic']=pic
		trip_context['type']="trips"
		return(trip_context)
		#print(trip_context_list)
		#return JsonResponse(trip_context_list, safe=False)

def create_trips(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session['sessionid']
				
				placeid=json.loads(request.body.decode('utf-8'))["placeid"]
				#trip_location=json.loads(request.body.decode('utf-8'))["triplocation"]
				travel_starting_date=json.loads(request.body.decode('utf-8'))["startingdate"]
				traveling_from=json.loads(request.body.decode('utf-8'))["travelingfrom"]
				traveling_to=json.loads(request.body.decode('utf-8'))["travelingto"]
				travel_ending_date=json.loads(request.body.decode('utf-8'))["endingdate"]
				noofcurrenttravelers=json.loads(request.body.decode('utf-8'))["noofcurrenttravelers"]
				noofrequiredtravelers=json.loads(request.body.decode('utf-8'))["noofrequiredtravelers"]
				prefferences=json.loads(request.body.decode('utf-8'))["prefference"]

				trip_planning=json.loads(request.body.decode('utf-8'))["tripplanning"]
				expenses_details=json.loads(request.body.decode('utf-8'))["expensesdetails"]
				phone_no=json.loads(request.body.decode('utf-8'))["phoneno"]
				email=json.loads(request.body.decode('utf-8'))["email"]
				trip_time=time.time()

				entry_trip=People_Trips(
																travel_starting_date=travel_starting_date,
																travel_ending_date=travel_ending_date,
																nooftravelerscurrent=noofcurrenttravelers,
																nooftravelersrequired=noofrequiredtravelers,
																trip_planning=trip_planning,
																traveling_from=traveling_from,
																traveling_to=traveling_to,
																preferences=prefferences,
																expenses_details=expenses_details,
																phone_number=phone_no,
																email=email,
																userid=People(sessionid),
																placeid=Place(placeid),
																time=trip_time
																)
				entry_trip.save()
				join_t=Join_table(post_trips=entry_trip,time=trip_time)
				join_t.save()
				return(JsonResponse(load_t(entry_trip),safe=False))
				#return HttpResponse()


def edit_trip(request,id=None):
		if request.method=="POST":
				#sessionid=request.session.get("sessionid")
				if request.session.get("sessionid",None):
					sessionid=request.session["sessionid"]
					tripid = json.loads(request.body.decode("utf-8"))['tripid']
					placeid = json.loads(request.body.decode("utf-8"))['placeid']
					travel_starting_date = json.loads(request.body.decode('utf-8'))["startingdate"]
					travelingfrom = json.loads(request.body.decode('utf-8'))["travelingfrom"]
					travelingto = json.loads(request.body.decode('utf-8'))["travelingto"]
					travel_ending_date = json.loads(request.body.decode('utf-8'))["endingdate"]
					noofcurrenttravelers = json.loads(request.body.decode('utf-8'))["noofcurrenttravelers"]
					noofrequiredtravelers = json.loads(request.body.decode('utf-8'))["noofrequiredtravelers"]
					prefferences = json.loads(request.body.decode('utf-8'))["prefferences"]

					trip_planning = json.loads(request.body.decode('utf-8'))["tripplanning"]
					expenses_details = json.loads(request.body.decode('utf-8'))["expensesdetails"]
					phone_no = json.loads(request.body.decode('utf-8'))["phoneno"]
					email = json.loads(request.body.decode('utf-8'))["email"]

					try:
							update_trip_obj = People_Trips.objects.get(tripid=tripid, userid=sessionid)

							if prefferences!= None:

									update_trip_obj.preferences = prefferences
									update_trip_obj.save()

							if travel_starting_date!=None:

									update_trip_obj.travel_starting_date=travel_starting_date
									update_trip_obj.save()

							if travel_ending_date!=None:

									update_trip_obj.travel_ending_date=travel_ending_date
									update_trip_obj.save()

							if noofcurrenttravelers!=None:

									update_trip_obj.nooftravelerscurrent=noofcurrenttravelers
									update_trip_obj.save()

							if noofrequiredtravelers!=None:

									update_trip_obj.nooftravelersrequired=noofrequiredtravelers
									update_trip_obj.save()

							if travelingfrom!=None:

									update_trip_obj.traveling_from=travelingfrom
									update_trip_obj.save()

							if travelingto!=None:

									update_trip_obj.traveling_to=travelingto
									update_trip_obj.save()

							if trip_planning!=None:

									update_trip_obj.trip_planning=trip_planning
									update_trip_obj.save()

							if expenses_details!=None:

									update_trip_obj.expenses_details=expenses_details
									update_trip_obj.save()

							if phone_no!=None:

									update_trip_obj.phone_number=phone_no
									update_trip_obj.save()

							if email!=None:

									update_trip_obj.email=email
									update_trip_obj.save()

					except Exception as e:
							print ("The exception is "+str(e))

				return HttpResponse()

def load_trips(request,id=None):
		if request.method=="POST":
				placeid=id
				trip_context_list=[]
				try:
						trip_obj=People_Trips.objects.all()
						print( trip_obj)

						for trips in trip_obj:
								tripid=trips.tripid
								#trip_location = trips.trip_location
								travel_starting_date = trips.travel_starting_date
								travel_ending_date = trips.travel_ending_date
								nooftravelerscurrent = trips.nooftravelerscurrent
								nooftravelersrequired = trips.nooftravelersrequired

								trip_plannning = trips.trip_planning
								expenses_details = trips.expenses_details
								preferences=trips.preferences
								phone_no = trips.phone_number
								travelingfrom=trips.traveling_from
								travelingto=trips.traveling_to
								email = trips.email
								userid = trips.userid
								time = trips.time
								pic=userid.photo



								try:
										trip_status_obj=People_Trips_Status.objects.get(tripid=tripid,userid=sessionid)
										status=trip_status_obj.status

								except Exception as e:
										print("hadha")
										print(e)
										status="None"
								try:
										trip_status_obj_like=People_Trips_Status.objects.filter(tripid=tripid,status='like')
										count_likes=len(trip_status_obj_like)
								except Exception as e:
										print("2")
										count_likes=0

								#user_obj = People.objects.get(peopleid=str(userid))

								try:
										trip_status_obj_superlike=People_Trips_Status.objects.filter(tripid=tripid,status='superlike')
										count_superlikes=len(trip_status_obj_superlike)
								except Exception as e:
										print("3")
										count_superlikes=0

								if userid:
										username=userid.username
										tripuserid=userid.peopleid

								try:
										trip_comment_obj=People_Trips_Comment.objects.filter(tripid=tripid)
										count_comment=len(trip_comment_obj)
								except Exception as e:
										print("3")
										count_comment=0

								trip_context={}
								trip_context['tripusername']=username
								trip_context['tripuserid']=tripuserid
								trip_context['tripid']=tripid
								#trip_context['triplocation']=trip_location
								trip_context['travelingfrom']=travelingfrom
								trip_context['travelingto']=travelingto
								trip_context['tripstartingdate']=travel_starting_date
								trip_context['tripendingdate']=travel_ending_date
								trip_context['noofcurrenttravelers']=nooftravelerscurrent
								trip_context['noofrequiredtravelers']=nooftravelersrequired
								trip_context['prefference']=preferences
								trip_context['tripplanning']=trip_plannning
								trip_context['expensesdetails']=expenses_details
								trip_context['tripphoneno']=phone_no
								trip_context['email']=email
								trip_context['status']=status
								trip_context['nooflikes']=count_likes
								trip_context['noofsuperlikes']=count_superlikes
								trip_context['noofcomments']=count_comment
								trip_context['sessionuserid']=sessionid
								trip_context['user_pic']=pic
								trip_context_list.append(trip_context)

				except Exception as e:
						p = 0
						print("agnivesh")
						print (e)
				print(trip_context_list)
				return JsonResponse(trip_context_list, safe=False)

def create_likes(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				tripid=json.loads(request.body.decode('utf-8'))['tripid']
				try:
						trip_status_obj=People_Trips_Status.objects.get(userid=sessionid,tripid=tripid)
						if trip_status_obj:
								status=trip_status_obj.status
								if status=='superlike':
										trip_status_obj.status='like'
										trip_status_obj.save()
								elif status=='like':
										trip_status_obj.status='none'
										trip_status_obj.save()
								elif status=='none':
										trip_status_obj.status='like'
										trip_status_obj.save()

				except Exception as e:
						entry_trip_status_obj=People_Trips_Status(userid=People(sessionid),tripid=People_Trips(tripid),status='like')
						entry_trip_status_obj.save()

				new_upvote_obj=People_Trips_Status.objects.get(tripid=tripid,userid=sessionid)

				newstatus=new_upvote_obj.status


				new_trip_status_like_obj=People_Trips_Status.objects.filter(userid=sessionid,tripid=tripid,status='like')
				count_new_likes=len(new_trip_status_like_obj)
				new_trip_status_superlike_obj=People_Trips_Status.objects.filter(userid=sessionid,tripid=tripid,status='superlike')
				count_new_superlikes=len(new_trip_status_superlike_obj)

				context_likes={}
				context_likes['sessionuserid']=sessionid
				context_likes['tripid']=tripid
				context_likes['placeid']=5
				context_likes['status']=newstatus
				context_likes['nooflikes']=count_new_likes
				context_likes['noofsuperlikes']=count_new_superlikes

				return JsonResponse(context_likes,safe=False)

def create_superlike(request,id=None):
		if request.method=="POST":
			#sessionid=request.session.get('sessionid')
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				tripid = json.loads(request.body.decode('utf-8'))["tripid"]
				try:
						trip_status_obj = People_Trips_Status.objects.get(tripid=tripid,userid=sessionid)
						status = trip_status_obj.status
						if status == 'like':
								trip_status_obj.status = 'superlike'
								trip_status_obj.save()
						elif status == 'superlike':
								trip_status_obj.status = 'none'
								trip_status_obj.save()
						elif status == 'none':
								trip_status_obj.status = 'superlike'
								trip_status_obj.save()

				except Exception as e:
						#print(e)
						entry_trip_status_obj = People_Trips_Status(userid=People(sessionid),  tripid=People_Trips(tripid), status='superlike')
						entry_trip_status_obj.save()
				new_upvote_obj = People_Trips_Status.objects.get(tripid=tripid, userid=sessionid)
				newstatus = new_upvote_obj.status
				new_trip_status_like_obj = People_Trips_Status.objects.filter(userid=sessionid,tripid=tripid,  status='like')
				count_new_likes = len(new_trip_status_like_obj)
				new_trip_status_superlike_obj = People_Trips_Status.objects.filter(userid=sessionid,tripid=tripid,status='superlike')
				count_new_superlikes = len(new_trip_status_superlike_obj)
				context_likes = {}
				context_likes['sessionuserid'] = sessionid
				context_likes['tripid'] = tripid
				context_likes['placeid'] = 5
				context_likes['status'] = newstatus
				context_likes['nooflikes'] = count_new_likes
				context_likes['noofsuperlikes'] = count_new_superlikes
				return JsonResponse(context_likes, safe=False)


def create_trip_report(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				tripid=json.loads(request.body.decode('utf-8'))["tripid"]
				report=json.loads(request.body.decode('utf-8'))["report"]
				try:
						trip_status_obj=People_Trips_Status.objects.get(tripid=tripid,userid=sessionid)
						trip_status_obj.report=report
						trip_status_obj.save()
				except Exception as e:
						entry_report_status_obj=People_Trips_Status(userid=sessionid,tripid=tripid,status='none',report=report)
						entry_report_status_obj.save()
			return HttpResponse()


def create_trip_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				tripid=json.loads(request.body.decode('utf-8'))["tripid"]
				comment=json.loads(request.body.decode('utf-8'))["comment"]
				entry_comment_obj=People_Trips_Comment(tripid=People_Trips(tripid),userid=People(sessionid),comment=comment)
				entry_comment_obj.save()
				new_trip_comment_obj=People_Trips_Comment.objects.filter(tripid=tripid)
				count_comments=len(new_trip_comment_obj)
				print(count_comments)
				return JsonResponse({'tripid':tripid,'noofcomments':count_comments,'tripcommentid':entry_comment_obj.tripcommentid},safe=False)



def load_trip_comments(request,id=None):
		if request.method=="POST":
				if request.session.get("sessionid",None):
					sessionid=request.session["sessionid"]
					tripid=json.loads(request.body.decode("utf-8"))["tripid"]
					print(tripid)
					try:
						trip_comment_obj=People_Trips_Comment.objects.filter(tripid=tripid)
						comment_context_list=[]
						for trip_comment in trip_comment_obj:
							tripid=str(trip_comment.tripid)
							tripcommentid=trip_comment.tripcommentid
							tripuserid=str(trip_comment.userid)
							tripcomment=trip_comment.comment

							user_obj=People.objects.get(peopleid=tripuserid)
							username=user_obj.username

							comment_context={}
							comment_context['tripid']=tripid
							comment_context['iseditable']=False
							comment_context['tripcommentid']=tripcommentid
							comment_context['tripuserid']=str(tripuserid)
							comment_context['tripcomment']=tripcomment
							comment_context['sessionuserid']=sessionid
							comment_context['user_pic']=user_obj.photo
							comment_context['username']=user_obj.username
							comment_context_list.append(comment_context)

					except Exception as e:
							print(e) 

							p=0
					print (comment_context_list)
					return JsonResponse(comment_context_list,safe=False)


def edit_trips_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				#sessionid=1
				#placeid=id
				tripid=json.loads(request.body.decode("utf-8"))["tripid"]
				tripcommentid=json.loads(request.body.decode("utf-8"))["tripcommentid"]
				newcomment=json.loads(request.body.decode("utf-8"))["tripcomment"]
				try:

					update_comment_obj=People_Trips_Comment.objects.get(tripid=tripid,tripcommentid=tripcommentid,userid=sessionid)
					update_comment_obj.comment=newcomment
					update_comment_obj.save()
					print ("hello")
				except Exception as e:
						print (str(e))
						p=0

				return HttpResponse()

def delete_trips_comment(request,id=None):
		if request.method=="POST":
				#sessionid=request.session.get("sessionid")
				if request.session.get("sessionid",None):
					sessionid=request.session["sessionid"]
					tripid=json.loads(request.body.decode("utf-8"))["tripid"]
					tripcommentid=json.loads(request.body.decode("utf-8"))["tripcommentid"]
					#print ("The requested parameters are "+str(sessionid)+" "+str(placeid)+" "+str(tripid)+" "+str(tripcommentid))
					try:
						trip_comment_obj=People_Trips_Comment.objects.get(tripid=tripid,tripcommentid=tripcommentid,userid=sessionid)
						trip_comment_obj.delete()
					except Exception as e:
							print (e)
							p=0
					count=len(People_Trips_Comment.objects.filter(tripid=tripid))
					return JsonResponse({'noofcomments':count},safe=False)

def delete_trips(request,id=None):
		if request.method=="POST":
				#sessionid=request.session.get("sessionid")
				sessionid=1
				#placeid=id
				tripid=json.loads(request.body.decode("utf-8"))["tripid"]
				try:
					trip_obj=People_Trips.objects.get(userid=sessionid,tripid=tripid)
					trip_obj.delete()
				except Exception as e:
						p=0

				return HttpResponse()


def delete_article(request,id=None):
		if request.Method=="POST":
				if request.session.get("sessionid",None):
					sessionid=request.session["sessionid"]
					articleid=json.loads(request.body.decode("utf-8"))['articleid']
					try:
						del_obj=People_Article.objects.get(userid=sessionid,articleid=articleid)
						del_obj.delete()
					except Exception as e:
							print(e)
		return HttpResponse()

def edit_article(request,id=None):
		if request.Method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				articleid=json.loads(request.body.decode("utf-8"))["articleid"]
				newarticletext=json.loads(request.body.decode("utf-8"))["articleid"]

				try:
					update_article_obj=People_Article.objects.get(userid=sessionid,articleid=articleid)
					update_article_obj.articletext=newarticletext
					update_article_obj.save()

				except Exception as e:
						print(e)

				return HttpResponse()
	

def voting(request,id=None):
		global no_like
		global no_superlike
		if request.method == "POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				articleid=json.loads(request.body.decode('utf-8'))["articleid"]
				
				try:
						article_obj = People_Article_Status.objects.get(articleid=articleid, userid=sessionid)
						status = article_obj.status
						if status =='superlike':

								article_obj.status ='like'
								article_obj.save()
						elif status == 'none':
								article_obj.status = 'like'
								article_obj.save()
						elif status=='like':
								article_obj.status='none'
								article_obj.save()

				except Exception as e:
						entry_upvote=People_Article_Status(articleid=People_Article(articleid),userid=People(sessionid),status='like')
						entry_upvote.save()

				new_article_obj = People_Article_Status.objects.get(articleid=articleid, userid=sessionid)
				newstatus=new_article_obj.status

				new_article_obj_status_like = People_Article_Status.objects.filter(articleid=articleid,status='like')
				count_new_obj_status_like = len(new_article_obj_status_like)
				new_article_obj_status_superlike=People_Article_Status.objects.filter(articleid=articleid,status='superlike')
				count_new_obj_status_superlike=len(new_article_obj_status_superlike)
				upvoting_context = {}
				upvoting_context['articleid'] = articleid
				upvoting_context['status'] = newstatus

				upvoting_context['nooflike'] = count_new_obj_status_like
				upvoting_context['noofsuperlike']=count_new_obj_status_superlike
				upvoting_context['sessionid']=sessionid
				#upvoting_context['noofunlike'] = no_unlike
				#article_list_upvote.extend(upvoting)
				return JsonResponse(upvoting_context, safe=False)


def supervoting(request,id=None):
		global no_like
		global no_unlike
		if request.method == "POST":
			if request.session.get("sessionid"):
				sessionid=request.session["sessionid"]
				articleid = json.loads(request.body.decode('utf-8'))["articleid"]
				try:
						article_obj = People_Article_Status.objects.get(articleid=articleid, userid=sessionid)
						status = article_obj.status
						if status == 'like':

								article_obj.status = 'superlike'
								article_obj.save()
						elif status == 'none':
								article_obj.status = 'superlike'
								article_obj.save()
						elif status == 'superlike':
								article_obj.status = 'none'
								article_obj.save()

				except Exception as e:
						entry_upvote = People_Article_Status(articleid=People_Article(articleid), userid=People(sessionid),
																									status='superlike')
						entry_upvote.save()

				new_article_obj = People_Article_Status.objects.get(articleid=articleid, userid=sessionid)
				newstatus = new_article_obj.status

				new_article_obj_status_like = People_Article_Status.objects.filter(articleid=articleid, status='like'
																																					 )
				count_new_obj_status_like = len(new_article_obj_status_like)
				new_article_obj_status_superlike = People_Article_Status.objects.filter(articleid=articleid, status='superlike'
																																							 )
				count_new_obj_status_superlike = len(new_article_obj_status_superlike)
				upvoting_context = {}
				upvoting_context['articleid'] = articleid
				upvoting_context['status'] = newstatus

				upvoting_context['nooflike'] = count_new_obj_status_like
				upvoting_context['noofsuperlike'] = count_new_obj_status_superlike
				upvoting_context['sessionid'] = sessionid
				# upvoting_context['noofunlike'] = no_unlike
				# article_list_upvote.extend(upvoting)
				return JsonResponse(upvoting_context, safe=False)


no_like = ''
no_unlike = ''


def load_article_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				articleid=json.loads(request.body.decode("utf-8"))["articleid"]
				try:
						comment_context_list=[]
						article_obj_comment=People_Article_Comment.objects.filter(articlecommentid=articleid)
						for articles in article_obj_comment:
								commentid=articles.commentid
								articlecommentid=articles.articlecommentid.articleid
								userid=str(articles.userid)
								comment=articles.commenttext
								#print("The request parameters are "+str(commentid)+" "+str(articlecommentid)+" "+str(userid)+" "+str(comment))
								user_obj=People.objects.get(peopleid=userid)
								username=user_obj.username
								comment_context={}
								comment_context['commentid']=commentid
								comment_context['articlecommentid']=articlecommentid
								comment_context['articlecommentuserid']=userid
								comment_context['commenttext']=comment
								comment_context['sessionuserid']=sessionid
								comment_context['iseditable']=False
								comment_context['username']=username

								comment_context['user_pic']=user_obj.photo
								comment_context_list.append(comment_context)
								print (comment_context)


				except Exception as e:
						print("The exception is "+str(e))
						p=0
				return JsonResponse(comment_context_list,safe=False)

def edit_article_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				articlecommentid=json.loads(request.body.decode("utf-8"))["articlecommentid"]
				commentid=json.loads(request.body.decode("utf-8"))["commentid"]
				newcomment=json.loads(request.body.decode("utf-8"))['comment']
				print(articlecommentid)
				print(commentid)

				try:
						update_comment_obj=People_Article_Comment.objects.get(userid=sessionid,articlecommentid=articlecommentid,commentid=commentid)
						update_comment_obj.commenttext=newcomment
						update_comment_obj.save()

				except Exception as e:
						p=0
						print(e)

				return HttpResponse()

def delete_article_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				articleid=json.loads(request.body.decode("utf-8"))['articleid']
				articlecommentid=json.loads(request.body.decode("utf-8"))['articlecommentid']
				try:
						comment_obj=People_Article_Comment.objects.get(userid=sessionid,articlecommentid=articleid,commentid=articlecommentid)
						comment_obj.delete()
				except Exception as e:
						print ("The exception is "+str(e))
				return HttpResponse()

def upvoting_comment(request):
		global no_like
		global no_unlike
		if request.method == "POST":
			if request.session.get("sessionid",None):
				comment_list_upvote = []
				sessionid = request.session['sessionid']
				articleid = request.POST['articleid']
				articlecommentid = request.POST['commentid']
				objs = People_Article_Comment_Status.objects.filter(articleid=articleid, userid=sessionid, articlecommentid=articlecommentid)
				if objs:
						status = objs.status
						if status == "LIKE":
								objs.delete()
						elif status == "UNLIKE":
								objs.status = "LIKE"

				elif not objs:
						objs = People_Article_Comment_Status(
								articleid=articleid,
								articlecommentid=articlecommentid,
								userid=sessionid,
								status="LIKE"
						)
						objs.save()
				no_like = People_Article_Status.filter(articleid=articleid, articlecommentid=articlecommentid,
																							 status="LIKE").count
				no_unlike = People_Article_Status.filter(articleid=articleid, articlecommentid=articlecommentid,
																								 status="UNLIKE").count
				objs = People_Article_Status.objects.filter(articleid=articleid, articlecommentid=articlecommentid,
																										userid=sessionid)
				if objs:
						status = objs.status
				elif not objs:
						status = ''
				upvoting_comment = {}
				upvoting_comment['articleid'] = articleid
				upvoting_comment['articlecommentid'] = articlecommentid
				upvoting_comment['status'] = status
				upvoting_comment['no_like'] = no_like
				upvoting_comment['no_unlike'] = no_unlike
				#comment_list_upvote.extend(upvoting)
				return render_to_response(upvoting_comment)
		else:
				return HttpResponse('<script>alert("method not post");</script>')


def downvoting_comment(request):
		global no_like
		global no_unlike
		if request.method == "POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				comment_list_downvote = []
				sessionid = request.session['sessionid']
				articleid = request.POST['articleid']
				commentid = request.POST['commentid']
				objs = People_Article_Comment_Status.objects.filter(articleid=articleid, userid=sessionid, articlecommentid=commentid)
				if objs:
						status = objs.status
						if status == "UNLIKE":
								objs.delete()
						elif status == "LIKE":
								objs.status = "UNLIKE"

				elif not objs:
						objs = People_Article_Comment_Status(
								articleid=articleid,
								articlecommentid=commentid,
								userid=sessionid,
								status="UNLIKE"
						)
						objs.save()
				no_like = People_Article_Status.filter(articleid=articleid, articlecommentid=commentid,
																							 status="LIKE").count
				no_unlike = People_Article_Status.filter(articleid=articleid, articlecommentid=commentid,
																								 status="UNLIKE").count
				objs = People_Article_Status.objects.filter(articleid=articleid, articlecommentid=commentid,
																										userid=sessionid)
				if objs:
						status = objs.status
				elif not objs:
						status = ''
				downvoting_comment = {}
				downvoting_comment['articleid'] = articleid
				downvoting_comment['articlecommentid'] = commentid
				downvoting_comment['status'] = status
				downvoting_comment['no_like'] = no_like
				downvoting_comment['no_unlike'] = no_unlike
				#comment_list_upvote.extend(downvoting)
				return render_to_response(downvoting_comment)
		else:
				return HttpResponse('<script>alert("method not post");</script>')

def create_article_report(request, id=None):
		if request.method == "POST":
				#placeid = id
				# sessionid=request.session.get('sessionid')
				sessionid = 1
				articleid = json.loads(request.body.decode('utf-8'))["articleid"]
				report = json.loads(request.body.decode('utf-8'))["report"]
				print("In the trip report view")
				try:
					article_status_obj = People_Article_Status.objects.get(articleid=articleid,  userid=sessionid)
					article_status_obj.report = report
					article_status_obj.save()
				except Exception as e:
					entry_report_status_obj = People_Article_Status(userid=People(sessionid), articleid=People_Article(articleid), 
																														status='none', report=report)
					entry_report_status_obj.save()

				return HttpResponse()

def create_article_comment(request,id=None):
		if request.method=="POST":
			if request.session.get("sessionid",None):
				sessionid=request.session["sessionid"]
				articleid=json.loads(request.body.decode('utf-8'))["articleid"]
				comment=json.loads(request.body.decode('utf-8'))["comment"]
				try:
						entry_comment_obj=People_Article_Comment(articlecommentid=People_Article(articleid),
																									 userid=People(sessionid),
																									 commenttext=comment)
						entry_comment_obj.save()
				except Exception as e:
						print (e)
				count_comments=People_Article_Comment.objects.filter(articlecommentid=articleid).count()
				#count_comments=len(new_article_comment_obj)
				return JsonResponse({'articleid':articleid,'noofcomment':count_comments,'commentid':entry_comment_obj.commentid})


def load_my_photo_post(sessionid):
		print ("In the load photo post view")
		try:
				photo_post_obj=People_Photo_Post.objects.filter(userid=sessionid).order_by("-time")
				photo_context_list=[]
				for photos in photo_post_obj:
						photo_context_list.append(load_photo(photos,sessionid=sessionid))
		except Exception as e:
				print("The exception is "+str(e))
		return JsonResponse(photo_context_list,safe=False)




def load_other_photo_post(sessionid,id):
		viewuserid=id
		print ("In the load photo post view")
		try:
				photo_post_obj=People_Photo_Post.objects.filter(userid=viewuserid)
				photo_context_list=[]
				for photos in photo_post_obj:
						photo_context_list.append(load_photo(photos,sessionid))
		except Exception as e:
				print("The exception is "+str(e))
		print (photo_context_list)
		return JsonResponse(photo_context_list,safe=False)


def load_otherarticles(sessionid,id):
		article_list = []
		viewuserid=id
		objs = People_Article.objects.filter(userid=viewuserid)
		for obj in objs:
				article_list.append(load_article(obj,sessionid=sessionid))
		print(article_list)
		return JsonResponse(article_list,safe=False)


def load_mytrips(sessionid):
		try:
				trip_obj=People_Trips.objects.filter(userid=sessionid).order_by("-time")
				trip_context_list=[]
				for trips in trip_obj:
						trip_context_list.append(load_t(trips,sessionid=sessionid))

		except Exception as e:
				p = 0
				print (e)
		return JsonResponse(trip_context_list, safe=False)


def load_othertrips(sessionid,id):
		viewuserid=id
		try:
				trip_obj=People_Trips.objects.filter(userid=viewuserid)
				trip_context_list=[]
				for trips in trip_obj:
						trip_context_list.append(load_t(trips,sessionid=sessionid))

		except Exception as e:
				p = 0
				print (e)
		print(trip_context_list)
		return JsonResponse(trip_context_list, safe=False)


def load_myarticles(sessionid):
	article_list = []
	viewuserid=id
	tagobj=Tag.objects.get(tagid=1)
	tagid=tagobj.tagid
	objs = People_Article.objects.filter(userid=sessionid).order_by("-time")
	for obj in objs:
			article_list.append(load_article(obj,sessionid=sessionid))
	return JsonResponse(article_list,safe=False)

def load_otherprofilehtml(request,id):
	username=None
	try:
		varid=id.split(".")
		id=varid[1]
	except Exception as e:
		i=0
	if request.session.get("sessionid",None):
		sessionid=request.session["sessionid"]
		username=People.objects.get(peopleid=sessionid).username
		pic=request.session["sessionpic"]
		other_user=People.objects.get(peopleid=id)
		try:
			follow=other_user.manytomanypeopleid.get(peopleid=sessionid)
			status=True
		except Exception as e:
			status=None
	#print(status)
	places_visited=other_user.manytomanyplacetype.filter(placetype=1).count()
	places_wished=other_user.manytomanyplacetype.filter(placetype=2).count()
	places_follow=other_user.manytomanyplacetype.filter(placetype=0).count()
	#aboutme=other_user.aboutme
	nooffollowers=other_user.manytomanypeopleid.count()
	return(render(request,"userprofile.html",{'username':username,'nooffollowers':nooffollowers,'sessionid':sessionid,'other_user':other_user,'pic':pic,"status":status,'aboutme':other_user.aboutme,'places_visited':places_visited,'places_wished': places_wished,' places_follow': places_follow,"point":other_user.point}))

def create_tips(request,id=None):
	if request.method=="POST":
		if request.session.get("sessionid",None):
			sessionid=request.session['sessionid']
			tiptitle=json.loads(request.body.decode("utf-8"))["tiptitle"]
			tipdetails=json.loads(request.body.decode("utf-8"))["tipdetails"]
			place_id=json.loads(request.body.decode("utf-8"))["placeid"]
			tipsposttime=time.time()
			try:
				tip=People_Tips(tiptitle=tiptitle,tipdetails=tipdetails,tipuserid=People(sessionid),placeid=Place(place_id),time=tipsposttime)
				tip.save()
			except Exception as e:
				print(e)
			join_t=Join_table(post_tip=tip,time=tipsposttime)
			join_t.save()

	return HttpResponse()

def load_tips(tip,sessionid=None,placeid=None):

	context_tip_list = []
	t=tip
	userid=t.tipuserid
	placename=tip.placeid.title
	#if userid.username:
		#userid=People.objects.get(peopleid=userid)
	#sessionid=request.session["sessionid"]
	try:
		context_tip = {}
		context_tip['tiptitle']=t.tiptitle
		context_tip['tipid']=t.tipid
		context_tip['tipdetails']=t.tipdetails
		context_tip['tipuserid']=str(t.tipuserid)

		tipuserid=t.tipuserid
		tipid=t.tipid
		try:
			user_obj=People.objects.get(peopleid=str(tipuserid))
			username=user_obj.username
		except Exception as e:
			print (e)
		context_tip['tipusername']=username
		context_tip['user_pic']=user_obj.photo
		try:
			tip_status_obj=People_Tips_Status.objects.filter(tipid=tipid,status=True)
			noofhelpful=len(tip_status_obj)
		except Exception as e:
			noofhelpful=0

		try:
			#print (tipid)
			newstatusobj=People_Tips_Status.objects.get(userid=sessionid,tipid=tipid)
			status=newstatusobj.status
		except Exception as e:
			status=False
			print (e)

		context_tip['status']=status
		context_tip['noofhelpful']=noofhelpful
		context_tip['type']="tips"
		context_tip['placename']=placename
		context_tip['sessionid']=sessionid


	except Exception as e:
		print (e)
	print(context_tip)
	return context_tip

def create_tip_status(request,id=None):
	if request.method=="POST":
		place_id=id
		#print("In the tip status view")
		sessionid=request.session.get("sessionid",None)
		#sessionid=1
		tipid=json.loads(request.body.decode("utf-8"))["tipid"]
		try:
			status_obj=People_Tips_Status.objects.get(tipid=tipid,userid=sessionid)
			status=status_obj.status
			if status==True:
				status_obj.delete()
				newstatus=False
				
				#obj1=People_Tips.objects.get(tipid=tipid)
				#obj1.no_helpful+=1
				#obj1.save()
			else:
				status_obj.status=True
				status_obj.save()
				newstatus=True
				#obj1 = People_Tips.objects.get(tipid=tipid)
				#obj1.no_helpful -= 1
				#obj1.save()

		except Exception as e:
			status_obj=People_Tips_Status(tipid=People_Tips(tipid),userid=People(sessionid),status=True)
			status_obj.save()
			newstatus=True
			#obj1 = People_Tips.objects.get(tipid=tipid)
			#obj1.no_helpful += 1
			#obj1.save()

		#new_status_obj=People_Tips_Status.objects.get(tipid=tipid,userid=sessionid)
		




		no_of_helpful_obj=People_Tips_Status.objects.filter(tipid=tipid,status=True)
		count_no_of_helpful=len(no_of_helpful_obj)

		context_like={}
		context_like['status']=newstatus
		context_like['noofhelpful']=count_no_of_helpful
		print (context_like)
	return JsonResponse(context_like,safe=False)

def delete_tips(request,id=None):
	if request.method=="POST":
		#sessionid=1
		sessionid=request.session.get("sessionid")
		tipid=json.loads(request.body.decode("utf-8"))['tipid']
		try:
			tip_obj=People_Tips.objects.get(tipid=tipid,tipuserid=sessionid)
			tip_obj.delete()

		except Exception as e:
			print (e)

	return HttpResponse()

def create_report(request,id=None):
	if request.method == "POST":
		place_id = id
		sessionid = request.session.get("sessionid", None)
		#sessionid=1
		tipid = json.loads(request.body.decode("utf-8"))["tipid"]
		newreport = json.loads(request.body.decode("utf-8"))["report"]
		try:
			status_obj = People_Tips_Status.objects.get(tipid=tipid, userid=sessionid)
			status_obj.report=newreport
			status_obj.save()
		except Exception as e:
			status_obj = People_Tips_Status(tipid=People_Tips(tipid), userid=People(sessionid),report=newreport)
			status_obj.save()
	return HttpResponse()

def create_follow_people(request,id=None):
	if request.method=="POST":
		#sessionid=request.session.get("sessionid")
		sessionid=1
		#viewuserid=request.GET.get("id",None)
		viewuserid=2

		people_obj = People.objects.get(peopleid=sessionid)
		try:

			other_people_obj=people_obj.manytomanypeopleid.get(peopleid=viewuserid)
			remove(other_people_obj)

		except Exception as e:
			print (str(e))
			people_obj.manytomanypeopleid.add(viewuserid)

		try:
			follow_people_obj=people_obj.manytomanypeopleid.get(peopleid=viewuserid)
			if follow_people_obj:
				status_follow=True

		except Exception as e:
			print(str(e))
			status_follow=False

		all_follow_people_obj=people_obj.manytomanypeopleid.all()
		count_followers=len(all_follow_people_obj)

		return JsonResponse({'nooffollowers':count_followers,'status_follow':status_follow},safe=False)
def load_people_follow_status(request,id=None):
	if request.method=="POST":
		#sessionid=request.session.get("sessionid")
		#viewuserid=request.GET.get("viewuserid")
		sessionid=1
		viewuserid=3
		people_obj = People.objects.get(peopleid=sessionid)
		try:
			follow_people_obj=people_obj.manytomanypeopleid.get(peopleid=viewuserid)
			if follow_people_obj:
				status_follow=True

		except Exception as e:
			status_follow=False

		try:
			all_follow_people_obj = people_obj.manytomanypeopleid.all()
			count_followers = len(all_follow_people_obj)
		except Exception as e:
			count_followers=0

		return JsonResponse({'nooffollowers':count_followers,'status_follow':status_follow},safe=False)
def create_follow_place(request,id=None):
	if request.method=="POST":
		#sessionid=request.session.get("sessionid")
		#placeid=id
		sessionid=1
		placeid=1

		people_obj=People.objects.get(peopleid=sessionid)
		try:
			place_obj=people_obj.manytomanyplaceid.get(place_id=placeid)
			remove(place_obj)

		except Exception as e:
			people_obj.manytomanyplaceid.add(placeid)

		try:
			place_follow_obj=people_obj.manytomanyplaceid.all()
			count_place_follow=len(place_follow_obj)

		except Exception as e:
			count_place_follow=0

		try:
			status_place_follow_obj=people_obj.manytomanyplaceid.get(place_id=placeid)
			if status_place_follow_obj:
				statusplacefollow=True

		except Exception as e:
			statusplacefollow=False

		return JsonResponse({'statusplacefollow':statusplacefollow,'countplacefollowes':count_place_follow},safe=False)

def load_place_follow_status(request,id=None):

	if request.method=="POST":
		sessionid=1
		placeid=1
		#placeid=id
		#sessionid=request.session.get("sessionid")
		people_obj=People.objects.get(peopleid=sessionid)
		try:
			status_place_follow_obj = people_obj.manytomanyplaceid.get(place_id=placeid)
			if status_place_follow_obj:
				statusplacefollow = True

		except Exception as e:
			statusplacefollow = False

		try:
			place_follow_obj = people_obj.manytomanyplaceid.all()
			count_place_follow = len(place_follow_obj)

		except Exception as e:
			count_place_follow = 0

		return JsonResponse({'statusplacefollow':statusplacefollow,'noofplacefollower':count_place_follow},safe=False)

def load_other_tips(sessionid,id):
	viewuserid=id
	try:
		tips_obj=People_Tips.objects.filter(tipuserid=viewuserid)
		tips_context_list=[]
		for tips in tips_obj:
			tips_context_list.append(load_tips(tips,sessionid=sessionid))
	except Exception as e:
		p = 0
		print (e)
	print(tips_context_list)
	return JsonResponse(tips_context_list, safe=False)


def create_article(request):
	i=0
	return HttpResponse()


def showarticle(request,id=None):
	try:
		if request.session.get("sessionid",None):
			article_obj=People_Article.objects.get(articleid=id)
			return render(request,"showarticle.html",{"article":load_article(article_obj,request.session["sessionid"])})
	except Exception as e:
		print(e)
		return HttpResponse()



def place_article(request):
	placeid = json.loads(request.body.decode("utf-8"))["placeid"]
	article_post=[]
	place_obj=Place.objects.get(place_id=placeid)
	articles_obj_list=place_obj.people_article_set.all()
	for article_obj in articles_obj_list:
		article_post.append(load_article(article_obj))

	return JsonResponse(article_post,safe=False)
	
def updateaboutme(request):
	if request.session.get("sessionid",None):
		sessionid=request.session["sessionid"]
		people_obj=People.objects.get(peopleid=sessionid)
		aboutme = json.loads(request.body.decode("utf-8"))["text"]
		print(aboutme)
		people_obj.aboutme=aboutme
		people_obj.save()
		print(people_obj.aboutme)
		return HttpResponse()


def load_place_tip(request):
	placeid = json.loads(request.body.decode("utf-8"))["placeid"]
	tips_obj_list=People_Tips.objects.filter(placeid=Place(placeid))
	tips_list=[]
	for tips_obj in tips_obj_list:
		if request.session.get("sessionid",None):
			tips_list.append(load_tips(tips_obj,request.session["sessionid"]))
		else :
			tips_list.append(load_tips(tips_obj))
	print("tips_list")
	print(tips_list)
	return JsonResponse(tips_list,safe=False)

		
