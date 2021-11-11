from drf_yasg.utils import swagger_auto_schema
from rest_framework import response
from rest_framework.decorators import api_view
from author.models import Author
from comment.documentation import NoSchemaTitleInspector
from likes.models import Like
from likes.serializers import LikeSerializer

from posts.models import Post
from rest_framework.response import Response

from .documentation import getLikesResponse

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
    operation_description="not paginated atm, kinda broken, need fixing, see todo^^^^",
    responses={200: getLikesResponse, 404: "author with given id not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
)
@api_view(["GET"])
def getLiked(request, authorId):

    try:
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("author does not exist", status=404)

    likes = Like.objects.filter(author=authorId).all()

    return Response({"type": "liked", "items": LikeSerializer(likes, many=True).data}, status=200)
