from django.contrib import admin
from django.db.models import fields

from nodes.models import Node

# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    
    list_display = ("url",'allowIncoming', 'allowOutgoing',
              'authRequiredIncoming',
              'authRequiredOutgoing', )
    
    
    fields = ['url','netloc', 'allowIncoming', 'allowOutgoing',
              'authRequiredIncoming',
              'authRequiredOutgoing',
              'incomingName',
              'outgoingName',
              'incomingPassword',
              'outgoingPassword']

admin.site.register(Node, NodeAdmin)