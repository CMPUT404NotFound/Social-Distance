from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    host = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ("type", "id", "displayName", "host", "url", "github", "profileImage")

    def get_type(self, obj):
        return "Author"

    def get_host(self, obj):
        return "temp place holder host name"

    def get_url(self, obj: Author):
        return "placeholderserice/author/" + obj.id

'''

{
    "type":"author",
    # ID of the Author
    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    # the home host of the author
    "host":"http://127.0.0.1:5454/",
    # the display name of the author
    "displayName":"Lara Croft",
    # url to the authors profile
    "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    # HATEOS url for Github API
    "github": "http://github.com/laracroft",
    # Image from a public domain
    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
}
    
'''