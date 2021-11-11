from drf_yasg import openapi

from likes.serializers import LikeSerializer


getLikesResponse = openapi.Response("A list of like belonging to this parent", LikeSerializer(many=True))
