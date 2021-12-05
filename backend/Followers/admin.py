from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db import models

from Followers.models import Follower, Follow_Request

# Register your models here.


class FollowersAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'receiver')


class FollowRequestAdmin(ModelAdmin):
    
    
    fields = ("requestor", "requestee")

    list_display = ("requestor", "requestee")



admin.site.register(Follower, FollowersAdmin)
admin.site.register(Follow_Request, FollowRequestAdmin)
