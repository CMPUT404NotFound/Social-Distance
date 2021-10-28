from rest_framework import serializers
from .models import posts
from backend.settings import SITE_ADDRESS

class PostsSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    host = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = posts
        fields = ("type", "post_id", "author_id", "title", "visibility")

    def get_type(self, obj):
        return "post"

 