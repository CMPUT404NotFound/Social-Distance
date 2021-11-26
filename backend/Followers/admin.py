from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from Followers.models import Follower

# Register your models here.


class FollowersAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'receiver')


admin.site.register(Follower, FollowersAdmin)
