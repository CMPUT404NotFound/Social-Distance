

from rest_framework import serializers
from .models import Author
from backend.settings import SITE_ADDRESS

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
        return SITE_ADDRESS if obj.host == "" else obj.host
    def get_url(self, obj: Author):
        return "placeholderserice/author/" + str(obj.id) 
    
    def to_representation(self, instance):
        stuff =  super().to_representation(instance)
        stuff['id'] = f"{SITE_ADDRESS}/author/{stuff['id'] }"
        return stuff
    


class LoginSerializer(serializers.Serializer):
    displayName = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    
class ForeignAuthorSerializer(serializers.Serializer):
    
    type =serializers.SerializerMethodField()

    id = serializers.CharField(required = True,)
    
    displayName = serializers.CharField(required = True)

    host = serializers.CharField(required = True)

    url = serializers.CharField(required = True)
    
    github = serializers.CharField(required = False, allow_blank=True)
    
    profileImage = serializers.CharField(required = False,  allow_blank=True)


    def get_type(self, obj):
        return "Author"