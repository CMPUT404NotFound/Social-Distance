from django.shortcuts import render

from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from author.token import expires_in, refreshToken


from author.models import *
from author.serializers import *
from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


@api_view(["GET"])
def getAllFollowers(request: Request, id):
    """
    GET to get a list of all authors, with pagination options
    POST to register a new author
    """
    if request.method == "GET":
        try:
            #author = Author.objects.get(pk=id)
            author = Author.objects.filter(sender__receiver=id)
            s = FollowerSerializer(
                author, context={'request': request}, many=True)
            return Response(s.data)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "PUT", "DELETE"])
def addFollower(request: Request, author_id, follower_id):
    if request.method == "PUT":
        try:
            receiver = Author.objects.get(pk=author_id)
            sender = Author.objects.get(pk=follower_id)
            follow = Follower.objects.create(sender=sender, receiver=receiver)
            # author.sender.add(follower)
            follow.save()
            return Response(status=status.HTTP_201_CREATED)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(pk=follower_id)
            follow = Follower.objects.get(sender=follower, receiver=author)
            follow.delete()
            return Response(status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "GET":
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(pk=follower_id)
            follow = Follower.objects.get(sender=follower, receiver=author)
            if follow:
                return Response(status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
