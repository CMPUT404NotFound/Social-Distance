from django.shortcuts import render

from django.contrib.auth import authenticate
from drf_yasg import openapi
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
from utils.request import checkIsLocal, ClassType, makeRequest, parseIncomingRequest, ParsedRequest, HttpRequest, returnGETRequest, makeMultipleGETs
import json
import requests
from typing import Union
from inbox.models import InboxItem



@swagger_auto_schema(
    method="get", 
    operation_description="Get a list of all followers of author_id",
    responses={
        200: "Successful retrieval",
        404: "Author not found",
    },
    tags=['followers'])
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
                origin = follower_id.split("~")[0]
                # print("TYPE: ", type(follower_id))
                object = checkIsLocal(str(just_id), ClassType.AUTHOR)
                print("object: ", object)
                # print("HERE checkIsLocal(follower_id)23: ", object.isLocal)
                if origin != "project-api-404.herokuapp.com":
                    #print("NEW TO QUERY FOREIGN: ", checkIsLocal(str(request)))
                    replace_with_slash_follower = follower_id.replace("~", "/")
                    full_foreign_id = "https://" + replace_with_slash_follower + "/"
                    result = makeRequest("GET", full_foreign_id)
                    json_content = json.loads(result.content)
                    if 100 < result.status_code < 300:
                        json_content = json.loads(result.content)
                        results.append(json_content)

                else:
                    print("NEW OBJ: ", Author.objects.get(pk=just_id))
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
@swagger_auto_schema(
    method="get", 
    operation_summary="Check whether a potential author_A is following the author_B",
    responses={
        200: openapi.Response("True if author_A is following author_B", AuthorSerializer),
        404: openapi.Response("Author_A or author_B not found")
    },
    tags=['followers'])
    
@swagger_auto_schema(
    method="put", 
    operation_summary="If author_id is local, then regardless of whether follower_id is local or foreign, let follower_id follow author_id. If author_id is foreign, follower_id must be local; will then send follow request to author_id's inbox.",
    responses={
        200: openapi.Response("Successfully sent to author_id inbox/Successfully create a a Follower object"),
        404: openapi.Response("author_id or follower_id not found/Follower object already exists")
    },
    tags=['followers'])
@swagger_auto_schema(
    method="delete", 
    operation_summary="Remove follower_id from author_id's followers",
    responses={
        200: openapi.Response("Successfully removed from author_id's followers"),
        404: openapi.Response("author_id or follower_id not found/Unsuccessful deletion")
    },
    tags=['followers'])

# @authentication_classes([TokenAuth(needAuthorCheck=["DELETE"])])
@api_view(["GET", "DELETE", "PUT"])
@parseIncomingRequest(methodToCheck=["GET", "DELETE", "PUT"], type= ClassType.AUTHOR)
# def addFollower(request: Request, author_id, follower_id):
def addFollower(request: Union[ParsedRequest, HttpRequest], author_id, follower_id):
    isRequestLocal = request.islocal
    # print("request.islocal: ", request.islocal) #HELLO:  c76413d1-00bc-4cb7-8ca6-282b0bfcb953 <- FOREIGN!! USE ME AS EXAMPLE!
    if request.method == "PUT":
        #PUT author/{full_id_to_follow}/follower/{our_id_full}, is full_id_to_follow local? if yes do below
        makeFollower = False
        makeFollowerRequest = False
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
                
                try:#removing the follow request onject
                    follow_request = Follow_Request.objects.get(requestor=follower_id, requestee=receiver)
                    follow_request.delete()
                    makeFollower = True
                except:
                    pass
                if makeFollower == False:
                    print("requestor: ", follower_id.split("~")[-1])
                    print("requestee: ", receiver.id)
                    follow_request = Follow_Request.objects.create(requestor=follower_id, requestee=receiver)
                    follow_request.save()

                    inbox_object = InboxItem.objects.create(author=receiver, type="F", contentId=follow_request.pk)
                    inbox_object.save()


                else:
                    follow = Follower.objects.create(sender=follower_id.split("~")[-1], receiver=receiver)
                    follow.save()

                # follow_request = Follow_Request.objects.get(requestor=follower_id, requestee=receiver)
                # follow = Follower.objects.create(sender=follower_id, receiver=receiver)
                # follow.save()
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
            print("local_author_serialize: ", local_author_serialize)
            print("full_foreign_id: ", full_foreign_id)
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
            print("RESULT: ", result)
            print("RESULT.CONTENT: ", result.content)
            print("RESULT.STATUS_CODE: ", result.status_code)
            if 200 <= result.status_code < 300:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            

            #-----MAKING REQUEST TO FOREIGN SERVER-----
            # #print("full_foreign_id: ", full_foreign_id)
            # result = makeRequest("GET", full_foreign_id) #json.loads(result.content)
            # print("GET REQUEST: ", json.loads(result.content), " ", type(result))
            # #Have to make POST request to foreign inbox here
            # print("BABA: ", Author.objects.get(pk=follower_id.split("~")[-1])) #follower id is local
            # local_author__id = Author.objects.get(pk=follower_id.split("~")[-1])
            # #Following.objects.create(author=local_author__id, following=json.loads(result.content))
            



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




def findFriends(author : Author, split = False):
    
    '''
    finds a list of string that are the ids of friends of the (local)author provided. 
    Note, this list of ids might be from the local server for foreign server.
    '''
    
    followers : List[QuerySet] = Follower.objects.filter(receiver = author).values("sender")
    
    print(followers)
    
    needFetch = []
    localids = []

    for follower in followers:
        id : str= follower["sender"]
        if id.startswith("http"):
            #if the id is a link, it's foreign author, make request
            needFetch.append(f"{id if id.endswith('/') else (id + '/')  }followers/{author.id}/")
        else:
            localids.append(id)
    print(localids)
    localFriends = []
    for id in localids:
        f = Follower.objects.filter(receiver = id).filter(sender = author.id).exists()
        if f:
            localFriends.append(id)
             
    responses = makeMultipleGETs(needFetch)
    
    foreignFriends = []
    for response in responses:
        obj = response[1]
        if obj.status_code >= 400:
            continue
        if obj.content.lower() != "true":
            continue
        #neither of the know falsy reponses are gotten, this link is prob a follower
        
        foreignFriends.append(response[0][:response[0].find("follower")])
    
    return localFriends + foreignFriends if not split else (localFriends, foreignFriends)


@swagger_auto_schema(
    method="get",
    operation_summary="find all friends of the given local author id",
    responses={
        200: openapi.Response("a list of local or foreign friends", AuthorSerializer(many = True)),
        404: "author not found"
    },
    tags=["followers"]
)
@api_view(["GET"])
def friendsView(request: Union[HttpRequest, Request], authorId:str):
    
    
    try:
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("author requested does not exists", status=404)
    
    ids: List = findFriends(author)
    
    output = []
    needFetch = []
    for id in ids:
        if id.startswith("http"):
            needFetch.append(id)
        else:
            try:
                author = Author.objects.get(pk = id)
                output.append(AuthorSerializer(author).data)
            except:
                output.append({"error": f"author with id {id} not found"})
            
    responses = makeMultipleGETs(needFetch)
    
    for response in responses:
        obj = response[1]
        if 200 <= obj.status_code < 400:
            output.append(json.loads(obj.content))
    
    return Response(output, status=200)

def findFollowers(author: Author):
    followers : List[QuerySet] = Follower.objects.filter(receiver = author).values("sender")
    return [follower["sender"] for follower in followers]

