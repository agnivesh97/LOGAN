from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import social_network
from social_network import views as socialview
import search
from search_app import views as search_view
from django.contrib import admin
from .views import(
	post_list,
	post_home,
	post_detail,
	post_update,
	post_delete,
	photolink,
	login_,
	register,
	homep,
	update_place,
	search,
	create_review,
	create_reviewStatus,
	create_reviewStatusReport,
	load_review,
	user_location,

	create_follow_people,
	create_follow_place,
	placesearch,
	hobbysearch,
	count_credibility_function,
	get_place_photo,
	adminloginview,
	get_hobbytags,
	contributors,
	profile_pic
	)
import edite_data
from edite_data import views as viewed

urlpatterns = [
	url(r'^profile/([^/]+)/$', socialview.profilehtml),
	url(r'^user/([^/]+)/$', socialview.load_otherprofilehtml),
	url(r'^$', post_home),
	url(r'^list/$', post_list),
	url(r'^place/([^/]+)/$',post_detail, name='detail'),
	url(r'^update/$',viewed.temp_update ),
	url(r'^showlist/$',viewed.showlist ),
	url(r'^adminlogin/$',adminloginview),
	url(r'^showedit/(\d+)/(\d+)/$',viewed.showedit),
	url(r'^delete/$', post_delete),
	url(r'^discover/$', photolink),
	url(r'^logan/$', photolink),
	url(r'^plogin/', login_),
	url(r'^register/', register),
	url(r'^updateapproved/(\d+)/$',update_place ),
	url(r'^home/$',homep),
	url(r'^search/$',search_view.search),
	url(r'^search/loadphoto/$',search_view.loadphotos),
	url(r'^searchresult/',search),
	url(r'^insert/(\d+)/$',create_review),
    url(r'^insert_status/(\d+)',create_reviewStatus),
    url(r'^insert_status_report/(\d+)',create_reviewStatusReport),
	url(r'^reviews/(\d+)/$',load_review),
	url(r'^userlocations/$',user_location),
	url(r'^posts/follow/$',create_follow_people),
	url(r'^posts/placefollow/$',create_follow_place),
	url(r'^searchplaces/$',placesearch),
	url(r'^searchhobby/$',hobbysearch),
	url(r'^count/$',count_credibility_function),
	url(r'^placephoto/$',get_place_photo),
	url(r'^hobbytags/$',get_hobbytags),
	url(r'^addplace/$',viewed.addplace),
	url(r'^contributors/$',contributors),
	url(r'^profile_pic/$',profile_pic),
	]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
