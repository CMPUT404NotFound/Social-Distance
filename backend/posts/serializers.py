from rest_framework import serializers
from .models import content_choice, visibility_choice, Post
from backend.settings import SITE_ADDRESS
from author.serializers import AuthorSerializer 
from comment.serializers import ChoiceField

class PostsSerializer(serializers.ModelSerializer):

    post_id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()

    source = serializers.SerializerMethodField()

    # url = serializers.SerializerMethodField()
    contentType = ChoiceField(choices=content_choice)
    visibility = ChoiceField(choices=visibility_choice)

    class Meta:
        model = Post
        fields = ("type", "post_id", "author", "title", 
        "visibility","description","content", "contentType",
        "source", "origin","counts","categories","comments","unlisted","published")

    def get_type(self, obj):
        return "post"
    def get_author(self, obj):
        return AuthorSerializer(obj.author_id).data
    def get_post_id(self, obj):
        return f"{SITE_ADDRESS}/author/{obj.author.id}/posts/{obj.post.id}"
