from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from Followers.models import Follower,Following

# Register your models here.


class FollowersAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'receiver')


class FollowingAdmin(ModelAdmin):

    fields = ("author", "following")
    

admin.site.register(Follower, FollowersAdmin)
admin.site.register(Following, FollowingAdmin)

