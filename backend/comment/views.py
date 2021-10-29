from django import http
from django.core import paginator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.

from rest_framework.decorators import (
    api_view,
)


from .models import Comment, Post
from .serializers import CommentSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from .documentation import NoSchemaTitleInspector, getCommentsResponse

from author.serializers import ForeignAuthorSerializer
from author.models import Author


@swagger_auto_schema(
    method="get",
    operation_description="paginated with 'page' and 'size'. Query without pagination to get all comments",
    operation_summary="Get comments of a post",
    responses={
        200: getCommentsResponse,
        400: "Bad path params or bad pagination",
        404: "Post not found",
    },
    field_inspectors=[NoSchemaTitleInspector],
    tags=["commments"],
)
@api_view(["GET", "POST"])
def handleComments(request: Request, authorId: str = "", postId: str = ""):

    if request.method == "GET":
        try:
            comments = Post.objects.get(pk=postId).post_comments.all()
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
            "post": "place holder post link",
            "id": "placeHolderLink/comments",  # todo fix these 2 placeholders once post is done.
            "comments": serial.data,
        }

        return Response(output, status=200)

    elif request.method == "POST":
        data = request.data

        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response("no post under this id", status=status.HTTP_404_NOT_FOUND)

        try:
            if (
                all(
                    (
                        item in data
                        for item in (
                            "type",
                            "author",
                            "comment",
                            "commentType",
                            "published",
                        )
                    )
                )
                and data["type"] == "comment"
            ):

                if "id" in data["author"]:  # just check if author has id
                    if Author.objects.filter(
                        pk=data["author"]["id"]
                    ).exists():  # since if the db has the id already, then all other info is already in the db
                        comment = Comment.objects.create(
                            author=Author.objects.get(pk=data["author"]["id"]),
                            comment=data["comment"],
                            commentType=data["commentType"],
                            published=data["published"],
                            post=post,
                        )
                        comment.save()
                        return Response(
                            "comment created", status=status.HTTP_204_NO_CONTENT
                        )
                    else:
                        pass  # handle foreign author
            else:
                return Response(
                    "Bad request! Are you sure all of ('type', 'author', 'comment', 'commentType', 'published') are provided in the request?",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except (KeyError,) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
