
import json

from author.models import *
from author.serializers import AuthorSerializer
from backend.settings import SITE_ADDRESS
from rest_framework import serializers
from utils.request import checkIsLocal, makeRequest

from Followers.models import Follow_Request


class FollowerSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    host = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ("type", "id", "displayName", "host",
                  "url", "github", "profileImage")

    def get_type(self, obj):
        return "Follower"

    def get_host(self, obj):
        # return "temp place holder host name"
        return SITE_ADDRESS

    def get_url(self, obj: Author):
        return "placeholderserice/author/" + str(obj.id)

class FollowRequestSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Follow_Request
        fields = []
        
    
    def to_representation(self, instance : Follow_Request):
        islocal = checkIsLocal(instance.requestor)
        
        
        if islocal.isLocal:
            try: 
                author = Author.objects.get(pk = islocal.id)
                follower = AuthorSerializer(author).data
            except Author.DoesNotExist:
                follower = {
                    "error": "the requested local author as follower no long exists"
                }
                
        else: 
            result = makeRequest("GET", islocal.long)
            
            if 200 <=result.status_code < 300:
                follower = json.loads(result.content)
            else:
                follower = {
                    "error": "the requested foreign author as follower no longer exist"
                }
        
        localAuthor :Author = instance.requestee # this author has to exist, since on_delete= Cascade
        
        
        
        repr = {
            "type" : "Follow",
            "summary": f"{follower['displayName']} wants to follow {localAuthor.displayName}",
            "actor": follower,
            "object": AuthorSerializer(localAuthor).data
        }
        
        return repr
        #to internal_val doesn't need to be implemented.
