from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from inbox.models import InboxItem

# Register your models here.

class InboxAdmin(ModelAdmin):
    
    
    fields = [
        'author',
        'type',
        'contentId'
    ]
    list_display =  [
        'author',
        'type',
        'contentId'
    ]
    
admin.site.register(InboxItem, InboxAdmin)