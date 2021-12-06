from typing import Union

from author.models import Author
from author.serializers import AuthorSerializer
from author.token import NodeBasicAuth, TokenAuth
from comment.documentation import NoSchemaTitleInspector
from comment.models import Comment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from inbox.models import InboxItem
from posts.models import Post
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from utils.request import ClassType, ParsedRequest, checkIsLocal, parseIncomingRequest, returnGETRequest, returnPOSTRequest

from likes.models import Like
from likes.serializers import LikeSerializer

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
@parseIncomingRequest(["GET"], ClassType.POST)
def getPostLikes(request: Union[HttpRequest, ParsedRequest], authorId, postId):

    if request.islocal:
        try:
            post = Post.objects.get(pk=request.id)
        except Post.DoesNotExist:
            return Response("post does not exist", status=404)

        likes = Like.objects.filter(parentId=request.id)

        return Response(LikeSerializer(likes.all(), many=True).data, status=200)
    else:
        return returnGETRequest(f"{request.id}likes")


@swagger_auto_schema(
    method="GET",
    operation_summary="get all likes of a comment",
    operation_description="not paginated atm, author and post id doesnt need to be real",
    responses={200: getLikesResponse, 404: "comment with given id not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
)
@api_view(["GET"])
@parseIncomingRequest(["GET"], ClassType.COMMENT)
def getCommentLikes(request, authorId, postId, commentId):
    if request.islocal:
        try:
            comment = Post.objects.get(pk=request.id)
        except Post.DoesNotExist:
            return Response("comment does not exist", status=404)

        likes = Like.objects.filter(parentId=request.id)
        # pagination not required
        return Response(LikeSerializer(likes.all(), many=True).data, status=200)
    else:
        return returnGETRequest(f"{request.id}likes")


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
@api_view(["GET"])
@parseIncomingRequest(["GET"])
def getLiked(request: Union[ParsedRequest, HttpRequest], authorId):

    if request.islocal:
        try:
            author = Author.objects.get(pk=request.id)
        except Author.DoesNotExist:
            return Response("author does not exist", status=404)

    if request.method == "GET":

        if not request.islocal:
            return returnGETRequest(f"{request.id}liked/")

        likes = Like.objects.filter(author=request.id).all()

        params = request.query_params

        if "page" in params and "size" in params:
            try:
                pager = Paginator(likes, int(params["size"]))
                serial = LikeSerializer(pager.page(int(params["page"])), many=True)
            except (ValueError, EmptyPage, PageNotAnInteger) as e:
                return Response(str(e), status=400)
        else:
            serial = LikeSerializer(likes, many=True)
        return Response({"type": "liked", "items": serial.data}, status=200)

    # elif request.method == "POST":
    #     # parse does not handle POST oops.
    #     # if not request.islocal:
    #     #     return Response("POSTing likes directly to other servers user is not allowed.", status=400)

    #     data = request.data
    #     try:
    #         target = data["target"]
    #         if pair := checkIsLocal(target):
    #             Like.objects.create(author=authorId, parentId=pair[0])
    #         else:
    #             Like.objects.create(author=authorId, parentId=target)
    #         return Response(status=204)

    #     except KeyError as e:
    #         return Response("bad request json format", status=400)


@swagger_auto_schema(
    method="post",
    operation_summary="(for frontend only)add a record of a local author liking a local or foreign post, and send the like to their inbox",
    operation_description="Note, no request body is needed, the semantics of this api is 'authorId' likes 'postId'. This post id can local or encoded foreign",
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
    responses={204: "like added", 400: "bad format", 404: "post to like, or author of the post is not found"},
)
@api_view(["POST"])
@parseIncomingRequest(["POST"], ClassType.POST)
@authentication_classes([TokenAuth(["POST"]), NodeBasicAuth])
def addLikePost(request: Union[ParsedRequest, HttpRequest], authorId, postId: str):

    if request.islocal:
        try:
            post: Post = Post.objects.get(pk=request.id)
            targetAuthorId = post.author_id.pk
        except Post.DoesNotExist:
            return Response("post not found!", status=404)

        if Like.objects.filter(author=authorId).filter(parentId = request.id):
            return Response(status = 204) #ignore like request if it exists already
        # this author id def exists, since it passed auth
        like = Like.objects.create(author=authorId, parentId=request.id)

        # post.author_id is linked a existing author via foreignkey
        InboxItem.objects.create(author=post.author_id, type="L", contentId=like.pk)
        return Response(status=204)
    else:
        foreignid = request.id[: request.id.find("post")]
        foreignid += "/" if not foreignid[-1] == "/" else ""

        data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": f"{request.user.displayName} likes your post",
            "type": "Like",
            "author": AuthorSerializer(request.user).data,
            "object": request.id,
        }

        return returnPOSTRequest(f"{foreignid}inbox/", data=data)


# feeling lazy
@swagger_auto_schema(
    method="post",
    operation_summary="(for frontend only)add a record of a local author liking a local or foreign comment, and send the like to their inbox",
    operation_description="Note, no request body is needed, the semantics of this api is 'authorId' likes 'commentId'. This comment id can local or encoded foreign",
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Likes"],
    responses={204: "like added", 400: "bad format", 404: "post to like, or author of the post is not found"},
)
@api_view(["POST"])
@parseIncomingRequest(["POST"], ClassType.COMMENT)
@authentication_classes([TokenAuth(needAuthorCheck=["POST"]), NodeBasicAuth])
def addLikeComment(request: Union[ParsedRequest, HttpRequest], authorId, commentId: str):

    if request.islocal:
        try:
            comment: Comment = Comment.objects.get(pk=request.id)
            targetAuthorId = comment.author
        except Comment.DoesNotExist:
            return Response("comment not found!", status=404)

        # this author id def exists, since it passed auth
        
        if Like.objects.filter(author=authorId).filter(parentId = request.id):
            return Response(status = 204) #ignore like request if it exists already
        
        like = Like.objects.create(author=authorId, parentId=request.id)
        try:
            targetAuthor = Author.objects.get(pk=targetAuthorId)
            InboxItem.objects.create(author=targetAuthor, type="L", contentId=like.pk)
        except Author.DoesNotExist:
            # if owner of the comment no longer exists, just simply skip sending inbox
            pass

        return Response(status=204)
    else:
        foreignid = request.id[: request.id.find("post")]
        foreignid += "/" if not foreignid[-1] == "/" else ""

        data = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": f"{request.user.displayName} likes your comment",
            "type": "Like",
            "author": AuthorSerializer(request.user).data,
            "object": request.id,
        }

        return returnPOSTRequest(f"{foreignid}inbox/", data=data)
