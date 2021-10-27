from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Author
import backend.settings as settings


class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField()

    host = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = (
            "type",
            "id",
            "displayName",
            "host",
            "url",
            "github",
            "profileImage",
        )

    def get_type(self, obj):
        return "author"

    def get_host(self, obj):
        return settings.SITE_ADDRESS

    def get_url(self, obj: Author):
        return f"{settings.SITE_ADDRESS}/{str(obj.id)}"


class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
