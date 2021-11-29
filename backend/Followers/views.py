from django.shortcuts import render

from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.authentication import TokenAuthentication
from author.token import expires_in, refreshToken, TokenAuth


from author.models import *
from author.serializers import *
from author.token import TokenAuth
from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from utils.request import checkIsLocal, ClassType, makeRequest
import json


@swagger_auto_schema(method="get", tags=['followers'])
@api_view(["GET"])
def getAllFollowers(request: Request, id):
    if request.method == "GET":
        try:
            #author = Author.objects.get(pk=id)
            #author = Author.objects.filter(sender__receiver=id)
            results = []
            # followers = Follower.objects.filter(receiver = id)
            follower_object = Follower.objects.filter(receiver = id)
            #print("follower_object: ", follower_object)
            for follower in follower_object:
                follower_id = follower.sender
                print("follower_id:", follower_id.split('id')[1][2: ]) #follower_id:  ['author: Bob, ', ': 6098687c-11f9-43ab-afa0-484a18b72356']
                just_id = follower_id.split('id')[1][2:]
                print("TYPE: ", type(follower_id))
                object = checkIsLocal(just_id, ClassType.author)
                print("HERE checkIsLocal(follower_id): ", object)
                if not object.isLocal:
                    response = makeRequest("GET", object.longId)
                    print("HERE response: ", response)
                    if 100 < response[1] < 300:
                        results.append(json.loads(response[0]))
                    





                results.append(AuthorSerializer(object).data)
            

            s = {
                'type': "followers",
                'items': results
            }
            return Response(s)
            # s = FollowerSerializer(
            #     author, context={'request': request}, many=True)
            # return Response(s.data)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#.TODO add speicial authentication for put
@swagger_auto_schema(method="get", tags=['followers'])
@swagger_auto_schema(method="put", tags=['followers'])
@swagger_auto_schema(method="delete", tags=['followers'])
@authentication_classes([TokenAuth(needAuthorCheck=["DELETE"])])
@api_view(["GET", "DELETE", "PUT"])
def addFollower(request: Request, author_id, follower_id):
    if request.method == "PUT":
        try:
            receiver = Author.objects.get(pk=author_id)
            sender = Author.objects.get(pk=follower_id)
            try:
                follower_exist = Follower.objects.get(
                    sender=follower_id, receiver=author_id)
                if follower_exist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
            follow = Follower.objects.create(sender=follower_id, receiver=follower_id)
            # author.sender.add(follower)
            follow.save()
            return Response(status=status.HTTP_201_CREATED)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(pk=follower_id)
            follow = Follower.objects.get(sender=follower_id, receiver=follower_id)
            follow.delete()
            return Response(status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "GET":
        try:
            author = Author.objects.get(pk=author_id)
            follower = Author.objects.get(pk=follower_id)
            follow = Follower.objects.get(sender=follower_id, receiver=follower_id)
            if follow:
                return Response(status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
