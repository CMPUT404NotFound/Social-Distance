from rest_framework import serializers

from backend.author.models import Author
from backend.author.serializers import AuthorSerializer
from .models import Like
from backend.settings import SITE_ADDRESS
from utils.request import makeRequest


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
            return makeRequest("GET", obj.author)

    def get_type(self, obj):
        return "Like"

    def get_object(self, obj):
        return obj.parentId

    def to_representation(self, obj):
        repr = super().to_representation(obj)
        repr["@context"] = "https://www.w3.org/ns/activitystreams"
        return repr
