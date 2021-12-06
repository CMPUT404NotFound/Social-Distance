from typing import Union
from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpRequest
from author.token import TokenAuth
from nodes.models import Node

from nodes.serializers import NodeSerializer
from utils.request import makeMultipleGETs, QueryResponse
# Create your views here.

import json

@api_view(["GET"])
@authentication_classes([TokenAuth(bypassEntirely=["GET"])])
def getNodes(request: Union[Request, HttpRequest]) -> Response:
    
    if request.method == "GET":
        return Response(NodeSerializer(Node.objects.all(), many = True).data, status=200)
    

@api_view(["GET"])
@authentication_classes([TokenAuth(bypassEntirely=["GET"])])
def getAllAuthors(request: Union[Request, HttpRequest]) -> Response:
    
    links = []
    
    node : Node
    for node in Node.objects.all():
        if node.allowOutgoing:
            links.append(f"{node.url}authors/")
    
    results = makeMultipleGETs(links)
    
    items = []
    for result in results:
        response = result[1]
        if response.status_code == 200:
            j = json.loads(response.content)
            try:
                stuff = j["items"]
            except KeyError:
                stuff = j["data"]
            items += stuff
    
    return Response({"type":"authors", "items" : items},status=200)