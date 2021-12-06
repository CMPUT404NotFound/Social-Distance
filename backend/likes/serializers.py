from rest_framework import serializers

from author.models import Author
from author.serializers import AuthorSerializer
from .models import Like
from utils.request import makeRequest
import json

from posts.models import Post
from comment.models import Comment
from backend.settings import SITE_ADDRESS
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("type", "author", "object")

    type = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        try:
            author = Author.objects.get(pk=obj.author)
            return AuthorSerializer(author).data
        except Author.DoesNotExist:
            return json.loads( makeRequest("GET", obj.author).content)

    def get_type(self, obj):
        return "Like"

    def get_object(self, obj):
        try: 
            post : Post = Post.objects.get(pk = obj.parentId)
            return f"{SITE_ADDRESS}author/{post.author_id.pk}/posts/{post.pk}/"
        except Exception as e:
            error = str(e)
            
        try: 
            comment: Comment = Comment.objects.get(pk = obj.parentId)
            return f"{SITE_ADDRESS}author/{comment.post.author_id.pk}/posts/{comment.post.pk}/comments/{comment.id}/"
        except Exception as e:
            error = str(e) + f" {obj.parentId}"
        
        print("error occured at get object, likes serialzier")
        return error + "like serializer"

    def to_representation(self, obj):
        repr = super().to_representation(obj)
        repr["@context"] = "https://www.w3.org/ns/activitystreams"
        return repr

        
