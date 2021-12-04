import json
from typing import Union

from author.models import Author
from author.token import TokenAuth
from backend.settings import SITE_ADDRESS
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from posts.models import Post as Post
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)

from rest_framework.response import Response
from utils.request import ClassType, ParsedRequest, parseIncomingRequest, returnGETRequest, returnPOSTRequest

from .documentation import NoSchemaTitleInspector, getCommentsResponse
from .models import Comment
from .serializers import CommentSerializer

# Create your views here.

def handleGET(request: Union[HttpRequest, ParsedRequest], authorId: str = "", postId: str = ""):
    if request.islocal:
        # handle local stuff
        try:
            post: Post = Post.objects.get(pk=request.id)  # request.id is the parsed post short id, since islocal is true
            comments = post.post_comments.all()
        except Post.DoesNotExist:
            return Response("no comments under this post", status=404)
        except ValidationError:
            return Response("Bad input.", status=400)

        params: dict = request.query_params

        if "page" in params and "size" in params:
            try:
                pager = Paginator(comments, int(params["size"]))
                serial = CommentSerializer(pager.page(int(params["page"])), many=True)
            except (ValueError, EmptyPage, PageNotAnInteger) as e:
                return Response(str(e), status=400)
        else:
            serial = CommentSerializer(comments, many=True)

        output = {
            "type": "comments",
            "page": params.get("page", 0),
            "size": params.get("size", 0),
            "post": f"{SITE_ADDRESS}author/{post.author_id.id}/posts/{post.post_id}/",
            # .TODO? this line seems uneeded"id": f"{SITE_ADDRESS}author/{post.author_id.id}/posts/{post.post_id}/comments/",
            "comments": serial.data,
        }

        return Response(output, status=200)
    else:
        # sent foreign request.

        return returnGETRequest(request.id)


def handlePOST(request: Union[HttpRequest, ParsedRequest], authorId: str = "", postId: str = ""):

    data = request.data  # jsonified body

    if request.islocal:
        try:
            post = Post.objects.get(pk=request.id)
        except Post.DoesNotExist:
            return Response("no post under this id", status=status.HTTP_404_NOT_FOUND)

        try:
            if all((item in data for item in ("type", "author", "comment", "contentType"))) and data["type"] == "comment":
                if "id" in data["author"]:  # just check if author has id

                    realAuthorId = data["author"]["id"].split("/author/")[-1]

                    if Author.objects.filter(pk=realAuthorId).exists():
                        # since if the db has the id already, then all other info is already in the db
                        comment = Comment.objects.create(
                            author=Author.objects.get(pk=data["author"]["id"]),
                            comment=data["comment"],
                            contentType=data["contentType"],
                            post=post,
                        )
                        comment.save()
                        return Response("comment created", status=status.HTTP_204_NO_CONTENT)
                    else:
                        # since author does not exist in current database, just save the id, to be looked up later
                        comment = Comment.objects.create(
                            author=data["author"]["id"],
                            comment=data["comment"],
                            contentType=data["contentType"],
                            post=post,
                        )
                        comment.save()
                        return Response("comment created", status=status.HTTP_204_NO_CONTENT)

                else:
                    return Response("bad formatting in author", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    "Bad request! Are you sure all of ('type', 'author', 'comment', 'contentType') are provided in the request?",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except (KeyError,) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    else:
        # make request to a foreign server, see utils.request.py
        return returnPOSTRequest(request.id, data)


@swagger_auto_schema(
    method="get",
    operation_description="paginated with 'page' and 'size'. Query without pagination to get all comments",
    operation_summary="Get comments of a post",
    responses={
        200: getCommentsResponse,
        400: "Bad path params or bad pagination",
        404: "Post not found",
    },
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
    field_inspectors=[NoSchemaTitleInspector],
    tags=["comments"],
)
@swagger_auto_schema(
    method="post",
    operation_summary="Create a comment",
    operation_description="""Create a comment for a post, id for comment does not need to be provided. In the author section,
    if the author is a local user, only the id is needed, if the author is a foreign user, the id, url, host, and displayName are needed.
    """,
    responses={
        204: "Comment created",
        400: "bad formatting on input (there's a lot of inputs here)",
    },
    request_body=CommentSerializer,
    field_inspectors=[NoSchemaTitleInspector],
    tags=["comments"],
)
@api_view(["GET", "POST"])
@authentication_classes([TokenAuth(needAuthorCheck=["POST"])])
@parseIncomingRequest(["GET", "POST"], ClassType.POST)
def handleComments(request: Union[HttpRequest, ParsedRequest], authorId: str = "", postId: str = ""):

    if request.method == "GET":

        return handleGET(request, authorId, postId)

    elif request.method == "POST":

        return handlePOST(request, authorId, postId)
