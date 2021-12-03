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
from utils.request import checkIsLocal, ClassType, makeRequest, parseIncomingRequest, ParsedRequest, HttpRequest, returnGETRequest
import json
import requests
from typing import Union


@swagger_auto_schema(method="get", tags=['followers'])
@api_view(["GET"])
@parseIncomingRequest(methodToCheck=["GET"], type= ClassType.AUTHOR)
def getAllFollowers(request: Union[ParsedRequest, HttpRequest], author_id):
    if request.method == "GET":
        try:
            results = []
            receiver_id = (request.id).split("/")[-1]
            print("receiver_id local?: ", receiver_id)
            follower_object = Follower.objects.filter(receiver = receiver_id)
            for follower in follower_object:
                print("follower.sender: ", follower.sender)
                follower_id = follower.sender #follower.sender:  project-api-404.herokuapp.com~api~author~5c6affc9-1bb7-4997-a82b-7e1ce4a9b17b
                print("follower_id.split 1~: ", follower_id.split("~")) #follower_id.split 1~:  ['project-api-404.herokuapp.com', 'api', 'author', '5c6affc9-1bb7-4997-a82b-7e1ce4a9b17b']
                just_id = follower_id.split("~")[-1]
                # print("TYPE: ", type(follower_id))
                object = checkIsLocal(str(just_id), ClassType.AUTHOR)
                print("object: ", object)
                # print("HERE checkIsLocal(follower_id)23: ", object.isLocal)
                if not object.isLocal:
                    #response = makeRequest("GET", object.longId)
                    url = "https://cmput404f21t17.herokuapp.com/service/author/" + str(follower_id) + "/"
                    response = requests.get(url) #c76413d1-00bc-4cb7-8ca6-282b0bfcb953/ <-- url
                    # print("HERE response: ", response)
                    if 100 < response.status_code < 300:

                        results.append(json.loads(response.content))

                else:
                    #print("NEW OBJ: ", Author.objects.get(pk=just_id))
                    new_obj_author_local = Author.objects.get(pk=just_id)
                    results.append(AuthorSerializer(new_obj_author_local).data)
            
            s = {
                'type': "followers",
                'items': results
            }
            return Response(s)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#.TODO add speicial authentication for put
@swagger_auto_schema(method="get", tags=['followers'])
@swagger_auto_schema(method="put", tags=['followers'])
@swagger_auto_schema(method="delete", tags=['followers'])
# @authentication_classes([TokenAuth(needAuthorCheck=["DELETE"])])
@api_view(["GET", "DELETE", "PUT"])
@parseIncomingRequest(methodToCheck=["GET", "DELETE", "PUT"], type= ClassType.AUTHOR)
# def addFollower(request: Request, author_id, follower_id):
def addFollower(request: Union[ParsedRequest, HttpRequest], author_id, follower_id):
    isRequestLocal = request.islocal
    # print("request.islocal: ", request.islocal) #HELLO:  c76413d1-00bc-4cb7-8ca6-282b0bfcb953 <- FOREIGN!! USE ME AS EXAMPLE!
    if request.method == "PUT":
        #PUT author/{full_id_to_follow}/follower/{our_id_full}, is full_id_to_follow local? if yes do below
        if isRequestLocal == True:
            try:
                receiver = Author.objects.get(pk=(request.id).split("/")[-1])
                follow_id_split = follower_id.split("~")[-1]
                try:
                    follower_exist = Follower.objects.get(
                        sender=follower_id, receiver=receiver)
                    if follower_exist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                except:
                    pass
                follow = Follower.objects.create(sender=follower_id, receiver=receiver)
                follow.save()
                return Response(status=status.HTTP_201_CREATED)
            except Author.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif isRequestLocal == False:
            # checkIsLocal(str(request))
            checkIsLocalResponse = checkIsLocal(str(request))
            #print("FOREIGN: ", (checkIsLocalResponse.id).replace("~", "/"), "--DONE--") #404.herokuapp.com~api~author~3190556a-dea8-47d1-a3b5-7c8a3e5c2f66/
            replace_with_slash = (checkIsLocalResponse.id).replace("~", "/")
            full_foreign_id = "https://" + replace_with_slash + "/"
            #print("full_foreign_id: ", full_foreign_id)
            result = makeRequest("GET", full_foreign_id) #json.loads(result.content)
            print("GET REQUEST: ", returnGETRequest(full_foreign_id), " ", type(result))
            #Have to make POST request to foreign inbox here

            return Response(status=status.HTTP_404_NOT_FOUND)


    elif request.method == "DELETE":
        
        try:
            receiver = Author.objects.get(pk=(request.id).split("/")[-1]) #will always be local
            follow = Follower.objects.get(sender=follower_id, receiver=receiver)
            follow.delete()
            return Response(status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "GET":
        try:
            author = Author.objects.get(pk=(request.id).split("/")[-1])
            print("author local?: ", author)
            follow = Follower.objects.get(sender=follower_id, receiver=author)
            if follow:
                return Response(status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
