from django.contrib import admin
from django.db.models import fields

from nodes.models import Node

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    
    list_display = ("url",'allowIncoming', 'allowOutgoing',
              
               )
    
    
    fields = ['url', 'allowIncoming', 'allowOutgoing',
              
              
              'incomingName',
              'outgoingName',
              'incomingPassword',
              'outgoingPassword', "description"]

admin.site.register(Node, NodeAdmin)