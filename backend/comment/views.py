from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from author.token import TokenAuth


from .models import Comment
from posts.models import Post as Post
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
def handleComments(request: Request, authorId: str = "", postId: str = ""):

    # todo verify if post's author is the same as the author privided in the url
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
            if all((item in data for item in ("type", "author", "comment", "contentType"))) and data["type"] == "comment":
                if "id" in data["author"]:  # just check if author has id
                    
                    realAuthorId = data["author"]["id"].split('/author/')[-1]
                    
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
                        #since author does not exist in current database, just save the id, to be looked up later
                        comment = Comment.objects.create(
                            author=data["author"]["id"],
                            comment=data["comment"],
                            contentType=data["contentType"],
                            post=post,
                        )
                        comment.save()
                        return Response("comment created", status=status.HTTP_204_NO_CONTENT)

                else:
                    return Response('bad formatting in author', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    "Bad request! Are you sure all of ('type', 'author', 'comment', 'contentType') are provided in the request?",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except (KeyError,) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
