import json

from drf_yasg import openapi

from author.models import Author
from author.token import TokenAuth, NodeBasicAuth
from comment.documentation import NoSchemaTitleInspector
from comment.models import Comment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from drf_yasg.utils import swagger_auto_schema
from Followers.models import Follow_Request
from Followers.serializers import FollowRequestSerializer
from likes.models import Like
from likes.serializers import LikeSerializer
from posts.models import Post
from posts.serializers import PostsSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from utils.request import makeMultipleGETs

from inbox.documentation import InboxItemSerializer
from inbox.models import InboxItem

from backend.settings import SITE_ADDRESS
# Create your views here.


def getAuthorId(request, authorId):
    authorid = request.data.get("author", None)
    if authorid is None:
        authorid = request.data.get("actor")["id"]
    else:
        authorid = authorid["id"]

    realAuthorId = authorid.split("/author/")[-1]

    if Author.objects.filter(pk=realAuthorId).exists():
        return realAuthorId
    return authorid


def handleLike(request, authorId):
    try:
        data = request.data
        authorid = getAuthorId(request, authorId)

        try:
            author = Author.objects.get(pk=str(authorId))
        except Author.DoesNotExist:
            return Response("Author does not exist", status=404)

        if "comment" in data["object"]:
            parentId = data["object"].split("/comment/")[-1]
            if not Comment.objects.filter(pk=parentId).exists():
                parentId = None
        elif "posts" in data["object"]:
            parentId = data["object"].split("/posts/")[-1]
            if not Post.objects.filter(pk=parentId).exists():
                parentId = None
        else:
            parentId = None

        if parentId:
            like = Like.objects.create(author=authorid, parentId=parentId)
            InboxItem.objects.create(author=author, type="L", contentId=like.pk)
            return Response(status=201)

        return Response("invalid id for comment or post", status=404)

    except KeyError:
        return Response("bad body format", status=400)


def handleFollows(request, authorId: str):
    try:
        follower = getAuthorId(request, authorId)

        try:
            author = Author.objects.get(pk=str(authorId))
        except Author.DoesNotExist:
            return Response("Author does not exist", status=404)


        try:
            author = Author.objects.get(pk = authorId)  # need varify the given author to follow exist in local db
            request = Follow_Request.objects.create(requestor=follower, requestee=author)
            InboxItem.objects.create(author=author, type="F", contentId=request.pk)
            return Response(status=204)
        except Author.DoesNotExist:
            return Response("author to follow not found", status=404)
    except KeyError:
        return Response("bad body format", status=400)


def handlePost(request, authorId):
    data = request.data

    try:
        id = data["id"].split("/posts/")[-1]
        try:
            author = Author.objects.get(pk=str(authorId))
        except Author.DoesNotExist:
            return Response("Author does not exist", status=404)

        if not Post.objects.filter(pk=id).exists():
            id = data["id"]

        InboxItem.objects.create(author=author, type="P", contentId=id)
        return Response(status=204)

    except KeyError:
        return Response("bad body format", status=400)


functions = {"like": handleLike, "follow": handleFollows, "post": handlePost}


def putItemInInbox(request, authorId: str):
    try:
        type = request.data["type"]
        return functions[type.lower()](request, authorId)
    except KeyError:
        return Response("'type' is not found", status=400)


def clearInbox(request, authorId):

    InboxItem.objects.filter(author=authorId).delete()
    return Response(status=204)


def getInboxItems(request, authorId):

    try:
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("author not found", status=404)

    items = InboxItem.objects.filter(author=author)

    needFetching = []
    itemsOutput = list(filter(
        lambda x: x != {} or x == None,
        [
            (
                {"F": FollowRequestSerializer, "P": PostsSerializer, "L": LikeSerializer}[item.type](
                    {"L": Like.objects.get, "P": Post.objects.get, "F": Follow_Request.objects.get,}[
                        item.type
                    ](**{"pk": item.contentId})
                ).data
                if {"L": Like.objects.filter, "P": Post.objects.filter, "F": Follow_Request.objects.filter,}[
                    item.type
                ](**{"pk": item.contentId}).exists()
                else needFetching.append(item.contentId) 
            )
            for item in items
        ],
    )).extend([response[1].content for response in makeMultipleGETs(needFetching)]) # woah dude
    # needFetching should really only contain posts' ids, since likes and follows's ids are always contained in the local database
    # but the serializers of Like and FollowRequest will still need to fetch remote data, which is sadly not included in the multi threaded fetch
    # fixing this will take some structural changes which i can't be bothered with, for the purpose of the project at least.

    params: dict = request.query_params

    if "page" in params and "size" in params:
        try:
            pager = Paginator(itemsOutput, int(params["size"]))
            itemsOutput = pager.page(int(params["page"]))
        except (ValueError, EmptyPage, PageNotAnInteger) as e:
            return Response(str(e), status=400)

    output = {
        "type": "inbox",
        "author": f"{SITE_ADDRESS}author/{authorId}",
        "items": [*itemsOutput],
    }

    return Response(output, status=200)


@swagger_auto_schema(
    method="POST",
    operation_summary="add a item to inbox",
    operation_description="add a item to an author's inbox, authentication needed. note any of the 3 types of inbox item are accepted, all 3 is not needed",
    responses={204: "adding inbox item success", 400: "bad request formatting", 404: "author id not found"},
    field_inspectors=[NoSchemaTitleInspector],
    request_body=InboxItemSerializer,
    tags=["Inbox"],
)
@swagger_auto_schema(
    method="DELETE",
    operation_summary="clear the entire inbox",
    operation_description="clear an author's inbox, authentication needed. ",
    responses={204: "inbox cleared"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Inbox"],
)
@swagger_auto_schema(
    method="GET",
    operation_summary="get inbox items",
    operation_description="get items in an author's inbox, authentication needed. Paginated.",
    responses={200: InboxItemSerializer, 400: "bag request or pagination", 404: "author not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Inbox"],
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
)
@api_view(["POST", "DELETE", "GET"])
@authentication_classes([TokenAuth(needAuthorCheck=["GET", "DELETE"]), NodeBasicAuth])
def handleInbox(request, authorId: str):
    print(request.method)
    if request.method == "POST":
        return putItemInInbox(request, authorId)
    elif request.method == "DELETE":
        return clearInbox(request, authorId)
    elif request.method == "GET":
        return getInboxItems(request, authorId)


