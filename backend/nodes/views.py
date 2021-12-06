from typing import Union
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpRequest
from author.token import TokenAuth
from author.documentations import NoSchemaTitleInspector
from nodes.models import Node

from nodes.serializers import NodeSerializer
from utils.request import makeMultipleGETs, QueryResponse

# Create your views here.

import json

from author.models import Author
from requests import get
from urllib.parse import urlparse


@api_view(["GET"])
@authentication_classes([TokenAuth(bypassEntirely=["GET"])])
def getNodes(request: Union[Request, HttpRequest]) -> Response:

    if request.method == "GET":
        return Response(NodeSerializer(Node.objects.all(), many=True).data, status=200)


@api_view(["GET"])
@authentication_classes([TokenAuth(bypassEntirely=["GET"])])
def getAllAuthors(request: Union[Request, HttpRequest]) -> Response:

    links = []

    node: Node
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

    return Response({"type": "authors", "items": items}, status=200)


# feeling lazy
@swagger_auto_schema(
    method="get",
    operation_summary="Gets recent public github events for this author, right now only supports pushEvents",
    responses={200: "im too tired to write this rn...... TODO FIXME", 404: "author not found, gitub link invalid etc"},
    field_inspectors=[NoSchemaTitleInspector],
    manual_parameters=[
        openapi.Parameter(
            name="page",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Page number",
            default=1,
        ),
        openapi.Parameter(
            name="size",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Page size",
            default=10,
        ),
    ],
    tags=["Github"],
)
@api_view(["GET"])
def getGithub(request: Union[Request, HttpRequest], authorId) -> Response:

    try:
        author: Author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("requested author for github lookup does not exist.", status=404)

    params: dict = request.query_params
    if "page" in params and "size" in params:
        per_page = params["size"]
        page = params["page"]
    else:
        per_page = 10
        page = 1

    parsed = urlparse(author.github)
    
    if parsed.netloc != "github.com" or parsed.path == "":
        return Response("This author has a invalid github link", status=404)
    
    path = parsed.path if parsed.path[-1] != "/" else parsed.path[:-1]
    checkExistance = get(f"https://api.github.com/users{path}", headers={"accept": "application/vnd.github.v3+json"})
    j = json.loads(checkExistance.content)
    
    if not "id" in j:
        return Response("The author's github link doesnt really exist", status=404)
    eventsResponse = get(
        f"http://api.github.com/users{path}/events?per_page={per_page}&page={page}", headers={"accept": "application/vnd.github.v3+json"}
    ).content
    eventsJson = json.loads(eventsResponse)

    # do stuff
    output = []
    print(json.dumps(eventsJson))
    for events in eventsJson:
        if events["type"] != "PushEvent":
            continue
        output.append(
            {
                "type": events["type"],
                "actor": events["actor"]["display_login"],
                "repo": events["repo"]["name"],
                "branch": events["payload"]["ref"][11:],
                "creationtime": events["created_at"],
                "commits": [
                    {"name": commit["author"]["name"], "email": commit["author"]["email"], "message": commit    ["message"]}
                    for commit in events["payload"]["commits"]
                ],
            }
        )

    return Response(output, status=200)

