from rest_framework import serializers

from author.models import Author
from author.serializers import AuthorSerializer
from .models import Like
from utils.request import makeRequest
import json

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
            return json.loads( makeRequest("GET", obj.author)[0])

    def get_type(self, obj):
        return "Like"

    def get_object(self, obj):
        return obj.parentId

    def to_representation(self, obj):
        repr = super().to_representation(obj)
        repr["@context"] = "https://www.w3.org/ns/activitystreams"
        return repr
