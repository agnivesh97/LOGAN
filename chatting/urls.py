from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from . import views
from .views import *
from django.contrib import admin

urlpatterns = [


	url(r'^messagehtml/$', views.messagehtml),
	url(r'^conversation/$', views.load_conversation_list),
	url(r'^message/(\d+)/$', views.load_messages),
	url(r'^pollingmessage/(\d+)/$', views.polling_message),
	url(r'^newmessage/(\d+)/$', views.create_conversation),

	#url(r'^la/$', views.load_article),
	#url(r'^up/$', views.voting),

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
