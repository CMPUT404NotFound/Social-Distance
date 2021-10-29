from rest_framework import serializers
from .models import posts
from backend.settings import SITE_ADDRESS
from author.serializers import AuthorSerializer 


class PostsSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()

    # host = serializers.SerializerMethodField()

    # url = serializers.SerializerMethodField()

    class Meta:
        model = posts
        fields = ("type", "post_id", "author_id", "title", "visibility","author","description","content","contentType")

    def get_type(self, obj):
        return "post"
    def get_author(self, obj):
        return AuthorSerializer(obj.author_id).data

   