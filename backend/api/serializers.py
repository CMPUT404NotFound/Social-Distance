from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.Serializer):
    testing = 'bruh'
    type = serializers.CharField()
    id = serializers.CharField()
    host = serializers.CharField()
    displayName = serializers.CharField()
    url = serializers.URLField()
    github = serializers.URLField()
    profileImage = serializers.URLField()
    
    
    
    
    
