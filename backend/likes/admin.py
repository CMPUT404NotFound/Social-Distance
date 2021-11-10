from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from likes.models import Like

# Register your models here.



class LikeAdmin(ModelAdmin):
    fields = ["author", "parentId"]
    
    
admin.site.register(Like, LikeAdmin)