from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views
from .views import *



urlpatterns = [
	#url(r'^$', post_home),
	url(r'^qa/(\d+)/$', views.load_question),
	url(r'^aa/(\d+)/$', views.load_answer),
	url(r'^pq/(\d+)/$', views.create_question),
	url(r'^pa/(\d+)/$', views.create_answer),
	url(r'^up/(\d+)/$', views.voting),
	url(r'^aup/(\d+)/$', views.answervoting),
	url(r'^dq/(\d+)/$', views.del_question),
	url(r'^da/(\d+)/$', views.del_answer),
	url(r'^ea/(\d+)/$', views.edit_answer),
	url(r'^rq/(\d+)/$', views.report),
	url(r'^ra/(\d+)/$', views.answerreport),


	url(r'^qahtml/$', views.qahtml),
	#url(r'^post_detail/(?P<id>\d+)/$',views.post_detail,name="detail"),
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
