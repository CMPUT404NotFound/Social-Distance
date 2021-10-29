
from typing_extensions import Required
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
        return "placeholderserice/author/" + str(obj.id) 
    


class LoginSerializer(serializers.Serializer):
    displayName = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    
class ForeignAuthorSerializer(serializers.Serializer):
    
    type =serializers.CharField()

    id = serializers.CharField(required = True)
    
    displayName = serializers.CharField(required = False)

    host = serializers.SerializerMethodField(required = False)

    url = serializers.SerializerMethodField(required = False)
    
    github = serializers.CharField(required = False)
    
    profileImage = serializers.CharField(required = False)


    