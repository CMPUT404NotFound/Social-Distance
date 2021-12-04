from django.shortcuts import render

from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
  
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from author.models import *
from author.serializers import *

from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from utils.request import checkIsLocal, ClassType, makeRequest, parseIncomingRequest, ParsedRequest, HttpRequest, returnGETRequest, makeMultiplieGETs
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
                if object.isLocal == False:
                    #print("NEW TO QUERY FOREIGN: ", checkIsLocal(str(request)))
                    replace_with_slash_follower = follower_id.replace("~", "/")
                    full_foreign_id = "https://" + replace_with_slash_follower + "/"
                    result = makeRequest("GET", full_foreign_id)
                    json_content = json.loads(result.content)
                    if 100 < result.status_code < 300:
                        json_content = json.loads(result.content)
                        results.append(json_content)

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
            replace_with_slash_local = follower_id.replace("~", "/")
            full_foreign_id = "https://" + replace_with_slash + "/"
            full_local_id = "https://" + replace_with_slash_local 
            local_author = Author.objects.get(pk=follower_id.split("~")[-1])
            local_author_serialize = AuthorSerializer(local_author).data

            foreign_object = makeRequest("GET", full_foreign_id)
            json_foreign_object = json.loads(foreign_object.content)
            data = {"type":"Follow","summary":"","actor":{
                        "type": local_author_serialize["type"],
                        "id": local_author_serialize["id"],
                        "displayName": local_author_serialize["displayName"],
                        "host": local_author_serialize["host"],
                        "url": local_author_serialize["url"],
                        "github": local_author_serialize["github"],
                        "profileImage": local_author_serialize["profileImage"]
                    },"object":{"type":"author",
                                "id":json_foreign_object.get("id"),
                                "url":json_foreign_object.get("url"),
                                "host":json_foreign_object.get("host"),
                                "displayName":json_foreign_object.get("displayName"),
                                "github":json_foreign_object.get("github"),
                                "profileImage":json_foreign_object.get("profileImage")}}
            result = makeRequest("POST", full_foreign_id + "inbox/", data)
            print("RESULT 1: ", result)

            

            #-----MAKING REQUEST TO FOREIGN SERVER-----
            # #print("full_foreign_id: ", full_foreign_id)
            # result = makeRequest("GET", full_foreign_id) #json.loads(result.content)
            # print("GET REQUEST: ", json.loads(result.content), " ", type(result))
            # #Have to make POST request to foreign inbox here
            # print("BABA: ", Author.objects.get(pk=follower_id.split("~")[-1])) #follower id is local
            # local_author__id = Author.objects.get(pk=follower_id.split("~")[-1])
            # #Following.objects.create(author=local_author__id, following=json.loads(result.content))
            

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




def findFriends(author : Author):
    
    '''
    finds a list of string that are the ids of friends of the (local)author provided. 
    Note, this list of ids might be from the local server for foreign server.
    '''
    
    followers : List[QuerySet] = Follower.objects.filter(receiver = author).values("sender")
    
    output = []
    needFetch = []
    localids = []

    for follower in followers:
        id : str= follower["sender"]
        if id.startswith("http"):
            #if the id is a link, it's foreign author, make request
            needFetch.append(f"{id if id.endswith('/') else (id + '/')  }followers/{author.id}/")
        else:
            localids.append(id)
    
    
    for id in localids:
        try:
            f = Follower.objects.get(receiver = id)
            output.append(id)
        except:
            pass
    
    responses = makeMultiplieGETs(needFetch)
    
    for response in responses:
        obj = response[1]
        if obj.status_code >= 400:
            continue
        if obj.content.lower() != "true":
            continue
        #neither of the know falsy reponses are gotten, this link is prob a follower
        
        output.append(response[0])
    
    return output



@api_view(["GET"])
def friendsView(request: Union[HttpRequest, Request], authorId:str):
    
    
    try:
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("author requested does not exists", status=404)
    
    ids = findFriends(author)
    
    