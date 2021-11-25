from typing import KeysView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from author.models import Author
from author.token import TokenAuth
from comment.documentation import NoSchemaTitleInspector
from likes.models import Like
from likes.serializers import LikeSerializer

from posts.models import Post
from rest_framework.response import Response
from rest_framework.request import Empty, Request

from .documentation import AddLike, getLikesResponse
from utils.request import checkIsLocal

# Create your views here.


@swagger_auto_schema(
    method="GET",
    operation_summary="get all likes of a post",
    operation_description="not paginated atm, author id doesn't need to be an real author, maybe this needs an update",
    responses={200: getLikesResponse, 404: "post with given id not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
)
@api_view(["GET"])
def getPostLikes(request, authorId, postId):

    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response("post does not exist", status=404)

    likes = Like.objects.filter(parentId=postId)

    return Response(LikeSerializer(likes.all(), many=True).data, status=200)


@swagger_auto_schema(
    method="GET",
    operation_summary="get all likes of a comment",
    operation_description="not paginated atm, author and post id doesnt need to be real",
    responses={200: getLikesResponse, 404: "comment with given id not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
)
@api_view(["GET"])
def getCommentLikes(request, authorId, postId, commentId):

    try:
        comment = Post.objects.get(pk=commentId)
    except Post.DoesNotExist:
        return Response("comment does not exist", status=404)

    likes = Like.objects.filter(parentId=commentId)

    return Response(LikeSerializer(likes.all(), many=True).data, status=200)


# todo make api endpoint for adding a like, when a local author likes a local or foreign content
@swagger_auto_schema(
    method="GET",
    operation_summary="get all likes from a author",
    operation_description="with pagination options ",
    responses={200: getLikesResponse, 404: "author with given id not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
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
@swagger_auto_schema(
    method="post",
    operation_summary="add a record of a local author liking a local or foreign media",
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
    responses={
        204: "like added",
        400: "bad format"
    },
    request_body= AddLike
)
@api_view(["GET", "POST"])
@authentication_classes([TokenAuth(needAuthorCheck=["POST"])])
def getLiked(request : Request, authorId):

    try:
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("author does not exist", status=404)

    if request.method == "GET":
        likes = Like.objects.filter(author=authorId).all()
        
        params = request.query_params
        
        if "page" in params and "size" in params:
            try: 
                pager = Paginator(likes, int(params['size']))
                serial = LikeSerializer(pager.page(int(params["page"]), many = True))
            except (ValueError, EmptyPage, PageNotAnInteger) as e:
                return Response(str(e), status=400)
        else:
            serial = LikeSerializer(likes, many=True)
        return Response({"type": "liked", "items": serial.data}, status=200)
    elif request.method == "POST":
        data = request.data
        try:
            target = data['target']
            if pair := checkIsLocal(target): 
                Like.objects.create(author = authorId,  parentId = pair[0])
            else:
                Like.objects.create(author = authorId,  parentId = target)
            return Response(status=204)
        
        except KeyError as e:
            return Response('bad request json format', status= 400)


