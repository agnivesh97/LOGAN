from django.shortcuts import render, get_object_or_404
import posts
from posts.models import *
from passlib.hash import pbkdf2_sha256
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from functools import reduce
from requests_oauthlib import OAuth2Session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import json,random,string,datetime,ast
#import os
from django.conf import settings as django_settings
import os
from django.shortcuts import redirect
from django.contrib import messages


from . import models
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

redirect_uri = 'http://localhost:8000/login/fblogin'
client_id = '299254863847343'
client_secret = 'b15151e9e0cadc1f4447332a0e32a6f7'
#log_file = os.path.join(django_settings.BASE_DIR,"exceptions.txt")
fb_state = ""

def index(request):
	return render(request, "hybrid_login/index.html")

def login_fb(request):
	q=request.GET.get("url",None)
	if q:
		request.session["url"]=q
	authorization_base_url = 'https://www.facebook.com/dialog/oauth/?scope=user_friends,email,public_profile'
	token_url = 'https://graph.facebook.com/oauth/access_token'
	#redirect_uri = 'https://pacific-shelf-88987.herokuapp.com/redirect_facebook/'
	facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
	facebook = facebook_compliance_fix(facebook)
	authorization_url, state = facebook.authorization_url(authorization_base_url)
	return HttpResponseRedirect(authorization_url)

def redirect_fb(request):
	if request.method=='GET':
		try:
			code=request.GET['code']
			state=request.GET['state']
		except Exception as e:
			if request.session.get("url",None):
				return HttpResponseRedirect("/place/"+request.session["url"]+"/")
			else:
				print("q1")
				return HttpResponseRedirect("/")
		else:
			if True:
				authorization_base_url = 'https://www.facebook.com/dialog/oauth/?scope=user_friends,email,public_profile'
				token_url = 'https://graph.facebook.com/oauth/access_token'
				facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
				facebook = facebook_compliance_fix(facebook)
				facebook.fetch_token(token_url, client_secret=client_secret, code=code)
				r1 = facebook.get('https://graph.facebook.com/v2.8/me/invitable_friends/?limit=500')
				r3 = facebook.get('https://graph.facebook.com/v2.8/me/friends/?limit=500')
				r2 = facebook.get('https://graph.facebook.com/v2.8/me?fields=id,name,email')
				entry = json.loads(r2.content.decode("utf-8"))
				context={}
				try:
					context['id']=entry['id']
					context['name']=entry['name']
					context['pic']="https://graph.facebook.com/"+entry['id']+"/picture?type=large"
					context['email']=entry['email']
					
					print("ok")
				except Exception as e:
					context['email']=""
				try:
					if context["email"]:
						people_object=get_object_or_404(People, email = context['email'])
					else:
						context['email']="none@none.com"
						people_object=get_object_or_404(People, userid = context['id'])
					request.session['sessionid'] = people_object.peopleid
					request.session['sessionpic'] = context['pic']
					print(request.session['sessionpic'])
					messages.info(request, 'Login success')
					if request.session.get("url",None):
						return HttpResponseRedirect("/place/"+request.session["url"]+"/")
					else:
						print("q2")
						return HttpResponseRedirect("/profile/"+people_object.username)    
				except Exception as e:
					hash = pbkdf2_sha256.encrypt(context['id'],rounds=500000, salt_size=32)
					entry1 = People(
						username=context['name'],
						email=context['email'],
						password=hash,
						photo=context['pic'],
						userid=context['id'],
						)
					entry1.save()
					people_object1=get_object_or_404(People,email=context['email'])
					request.session['sessionid']=people_object1.peopleid
					request.session['sessionpic']=context['pic']
					if request.session.get("url",None):
						return HttpResponseRedirect("/place/"+request.session["url"]+"/")
					else:
						print("q3")
						return HttpResponseRedirect("/profile/"+context['name'])
def login_google(request):
	q=request.GET.get('url',None)
	print("q agni")
	print(q)
	if q:
		request.session['url']=q
		
	client_id = '762392110250-pj80v4b83mnqruv81mi9t6hv84234ol7.apps.googleusercontent.com'
	client_secret = 'SUTtdmLL60TwS_TDTFNd_jW5'
	redirect_uri = 'http://localhost:8000/login/gologin/'

	# OAuth endpoints given in the Google API documentation
	authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
	token_url = "https://www.googleapis.com/oauth2/v4/token"
	scope = [
		"https://www.googleapis.com/auth/userinfo.email",
		"https://www.googleapis.com/auth/userinfo.profile"
	]

	google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

	# Redirect user to Google for authorization
	authorization_url, state = google.authorization_url(authorization_base_url, access_type="offline",
														approval_prompt="force")

	return HttpResponseRedirect(authorization_url)

def redirect_google(request):
	client_id = '762392110250-pj80v4b83mnqruv81mi9t6hv84234ol7.apps.googleusercontent.com'
	client_secret = 'SUTtdmLL60TwS_TDTFNd_jW5'
	redirect_uri = 'http://localhost:8000/login/gologin/'
	token_url = "https://www.googleapis.com/oauth2/v4/token"
	scope = [
		"https://www.googleapis.com/auth/userinfo.email",
		"https://www.googleapis.com/auth/userinfo.profile"
		]
	if request.method=='GET':
		try:
			code=request.GET['code']
			state=request.GET['state']
		except Exception as e:
			if request.session.get("url",None):
				return HttpResponseRedirect("/place/"+request.session["url"]+"/")
			else:
				print("q1")
				return HttpResponseRedirect("/")
		else:
			if True:
				#redirect_response = input('Paste the full redirect URL here:')

				# Fetch the access token
				google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
				google.fetch_token(token_url, client_secret=client_secret,code=code)

				# Fetch a protected resource, i.e. user profile
				r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
				entry = json.loads(r.content.decode("utf-8"))
				context = {}
				try:
					context['id'] = entry['id']
					context['name'] = entry['name']
					context['email'] = entry['email']
					context['pic'] = entry['picture']
				except Exception as e:
					return HttpResponse("<script>alert('email Required');</script>")
				#return render(request,"showdata.html",context)
				try:
					people_object = get_object_or_404(People, email=context['email'])
					request.session['sessionid'] = people_object.peopleid
					request.session['sessionpic'] = context['pic']
					messages.info(request, 'Login success')
					if request.session.get("url",None):
						q=request.session['url']
						del request.session['url']
						return HttpResponseRedirect("/place/"+q+"/")

					else:
						print("q1")
						return HttpResponseRedirect("/profile/"+people_object.username)
					# messages.add_message(request, messages.ERROR, 'Email already taken.')
				except Exception as e:
					hash = pbkdf2_sha256.encrypt(context['id'], rounds=500000, salt_size=32)
					entry2 = People(
						username=context['name'],
						email=context['email'],
						password=hash,
						photo=context['pic'],
					)
					entry2.save()
					people_object1 = get_object_or_404(People, email=context['email'])
					request.session['sessionid'] = people_object1.peopleid
					request.session['sessionpic'] = context['pic']
					#return HttpResponseRedirect(request, "home_page.html")

					if request.session.get("url",None):

						q=request.session['url']
						del request.session['url']
						return HttpResponseRedirect("/place/"+q+"/")
					else:
						print("q1")
						return HttpResponseRedirect("/profile/"+context['name'])
