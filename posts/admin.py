from django.contrib import admin
#from embed_video.admin import AdminVideoMixin
import edite_data
import question_answer
from question_answer.models import *
from edite_data.models import *
import search_reapp
from search_app.models import *
 


from .models import *


class PlaceInline(admin.TabularInline):
    model = Place_t
    extra = 0


class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        PlaceInline,
    ]


admin.site.register(Place_t, PlaceAdmin)


# Register your models here.
#admin.site.register(Place)
admin.site.register(People)
admin.site.register(PlaceType)
admin.site.register(Place_Follow)
admin.site.register(Photos)
admin.site.register(Videos)
admin.site.register(People_Place)
admin.site.register(People_Question)
admin.site.register(People_Answer)
admin.site.register(People_Question_Status)
admin.site.register(People_Answer_Status)
admin.site.register(People_Article)
admin.site.register(People_Article_Comment)
admin.site.register(People_Article_Status)
admin.site.register(People_Article_Comment_Status)
admin.site.register(Place_temp)
admin.site.register(Place, YourModelAdmin)
admin.site.register(Review_place)
admin.site.register(Review_place_status)
admin.site.register(Admin_notification)
admin.site.register(states)
admin.site.register(hobbytag)
admin.site.register(features)
admin.site.register(extra_tag)
admin.site.register(People_Photo_Post)
admin.site.register(People_Trips)
admin.site.register(People_Photo_Post_Status)
admin.site.register(Join_table)
admin.site.register(Tag)
admin.site.register(Tag_Article)
admin.site.register(People_Trips_Status)
admin.site.register(People_Tips)
admin.site.register(People_Tips_Status)
admin.site.register(People_Photo_Post_Comment)
admin.site.register(conversation)
admin.site.register(message)
admin.site.register(Adminlogin)
admin.site.register(New_place)
admin.site.register(User_record)
admin.site.register(user_profile_pic)

# Register your models here.
