from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from . import views
from .views import *
from django.contrib import admin


urlpatterns = [
	#url(r'^$', post_home),
	#url(r'^qa/(\d+)/$', views.load_question),
	#url(r'^aa/(\d+)/$', views.load_answer),
	#url(r'^pq/(\d+)/$', views.create_question),
	#url(r'^pa/(\d+)/$', views.create_answer),
	#url(r'^up/(\d+)/$', views.voting),
	#url(r'^aup/(\d+)/$', views.answervoting),


	url(r'^profilehtml/$', views.profilehtml),
	url(r'^profile/([^/]+)/$', views.profilehtml),
	url(r'^lapage/$', views.postarticlepagehtml),


	url(r'^lt/(\d+)/$', views.load_trips),
	url(r'^tsl/(\d+)/$', views.create_superlike),
	url(r'^tl/(\d+)/$', views.create_likes),
	url(r'^ltc/(\d+)/$', views.load_trip_comments),
	url(r'^ptc/(\d+)/$', views.create_trip_comment),
	url(r'^etc/(\d+)/$', views.edit_trips_comment),
	url(r'^dtc/(\d+)/$', views.delete_trips_comment),
	url(r'^ctr/(\d+)/$', views.create_trip_report),
	url(r'^dt/(\d+)/$', views.delete_trips),
	url(r'^lp/(\d+)/$', views.load_photo_post),
	url(r'^psl/(\d+)/$', views.create_photo_post_superlike),
	url(r'^pl/(\d+)/$', views.create_photo_post_like),
	url(r'^cpr/(\d+)/$', views.create_photo_report),
	url(r'^dpc/(\d+)/$', views.delete_photo_post_comment),
	url(r'^lpc/(\d+)/$', views.load_photo_post_comment),
	url(r'^ppc/(\d+)/$', views.create_photo_post_comment),
	url(r'^epc/(\d+)/$', views.edit_photo_post_comment),
	url(r'^la/(\d+)/$', views.load_article),
	url(r'^asl/(\d+)/$', views.supervoting),
	url(r'^al/(\d+)/$', views.voting),
	url(r'^car/(\d+)/$', views.create_article_report),
	url(r'^lac/(\d+)/$', views.load_article_comment),
	url(r'^pac/(\d+)/$', views.create_article_comment),
	url(r'^eac/(\d+)/$', views.edit_article_comment),
	url(r'^dac/(\d+)/$', views.delete_article_comment),
	url(r'^tp/(\d+)/$', views.create_trips),
	url(r'^pp/(\d+)/$', views.create_photo),
	url(r'^ca/(\d+)/$', views.create_article),
	url(r'^user/(\d+)/$', views.load_otherprofilehtml),
	url(r'^user/([^/]+)/$', views.load_otherprofilehtml),
	url(r'^dp/(\d+)/$', views.delete_photo_post),
	url(r'^et/(\d+)/$', views.edit_trip),
	url(r"^upload_image$", views.upload_image, name="upload_image"),
	url(r'^loadtips/(\d+)/$', views.load_tips),
	url(r'^posttips/(\d+)/$', views.create_tips),
	url(r'^deletetips/(\d+)/$', views.delete_tips),
	url(r'^liketips/(\d+)/$', views.create_tip_status),
	url(r'^reporttips/(\d+)/$', views.create_report),
	url(r'^showarticle/(\d+)/$', views.showarticle),
	url(r'^loadarticle/$', views.place_article),
	url(r'^updateaboutme/$', views.updateaboutme),
	url(r'^loadtips/$', views.load_place_tip),
	url(r'^tipsreport/$', views.create_report),
	url(r'^share/$', views.share),
    #url(r"^upload_image_validation", views.upload_image_validation, name="upload_image_validation"),



	#url(r'^post_detail/(?P<id>\d+)/$',views.post_detail,name="detail"),
	#url(r'^update/$', post_update),
	#url(r'^update/$', post_update),
	#url(r'^delete/$', post_delete),
	#url(r'^logan/', photolink),
	#url(r'^$', views.index_),
	#url(r'^register/$', views.register),
	#url(r'^login/$', views.login_),

]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
