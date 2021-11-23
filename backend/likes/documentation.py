from django.db.models.fields import CharField
from drf_yasg import openapi
from rest_framework import serializers

from likes.serializers import LikeSerializer


getLikesResponse = openapi.Response("A list of like belonging to this parent", LikeSerializer(many=True))

class AddLike(serializers.Serializer):
    target = serializers.CharField()