from os import stat
from django.utils.functional import empty
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Empty, Request
from rest_framework.decorators import (
    api_view,
    authentication_classes
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)


from author.models import Author
from author.serializers import AuthorSerializer
from comment.documentation import NoSchemaTitleInspector

from .models import Post

from .serializers import PostsSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from author.token import expires_in, refreshToken, TokenAuth

@swagger_auto_schema(method="get", tags=['Posts'])
@swagger_auto_schema(method="post", tags=['Posts'],field_inspectors=[NoSchemaTitleInspector],request_body=PostsSerializer)
@swagger_auto_schema(method="delete", tags=['Posts'],)
@swagger_auto_schema(method="put", tags=['Posts'],field_inspectors=[NoSchemaTitleInspector],request_body=PostsSerializer)
@authentication_classes([TokenAuth(needAuthorCheck=["POST","PUT", "DELETE"])])
@api_view(["GET","POST","DELETE","PUT"])
def managePost(request: Request, author_id, post_id):
    try:
        author = Author.objects.get(pk = author_id)
    except Author.DoesNotExist:
        return Response("no author under this id", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        try:
            post = Post.objects.filter(pk = post_id)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = PostsSerializer(post,context={"request": request}, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        s = PostsSerializer(request.data)
        if s.is_valid():
            s.save(author, post_id)
        return Response("Post created",s.data,status=status.HTTP_201_CREATED)

    elif request.method == "POST":
        try:  
            post : Post = Post.objects.filter(pk = post_id)
        except:  
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = PostsSerializer(instance=post, data=request.data)

        if s.is_valid():
            
            # post.visibility = s.visibility
            # post.title = s.title
            # post.description = s.description
            # post.content = s.content
            # post.contentType = s.contentType
            # post.source = s.source
            # post.unlisted = s.unlisted
            # post.published = s.published
            # post.count = s.count
            # post.categories = s.categories
            
            post.save()
            
            return Response("Post updated",s.data, status=status.HTTP_200_OK)
        return Response("Post not updated", status=status.HTTP_400_BAD_REQUEST)


    elif request.method == "DELETE":
        try: 
            post = Post.objects.filter(pk = post_id)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response("Post deleted", status=status.HTTP_204_NO_CONTENT)


# Create your views here.
@swagger_auto_schema(method="get",tags=['Posts'],
                     operation_summary="Get posts of an author",
                     operation_description="Get posts of author, with page & size pagination option. Request with no pagination to get all",
                     field_inspectors=[NoSchemaTitleInspector],
                     responses={200: PostsSerializer(many=True),
                                400: "Bad pagination format",
                                404: "Author or post not found"
                                }, 
                     )
                    
@swagger_auto_schema(method="post",tags=['Posts'],
                     operation_summary="Create a post",
                      field_inspectors=[NoSchemaTitleInspector],
                      responses={204: "Post Created Successfully.",
                                 400: "Bad post creation json format.",
                                 404: "Author not found."
                                 },
                      request_body=PostsSerializer
                     )
@api_view(["GET","POST"])
def getAllPosts(request: Request, author_id):
    # if request.method == "GET":
    #     try:
    #         #pagination
    #         post = posts.objects.filter(author_id=author_id)
    #         s = PostsSerializer(post, context={"request": request}, many=True)
    #         return Response(s.data)
            
    #     except posts.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
      
    if request.method == "GET":
        try:

            params: dict = request.query_params

            post = Post.objects.filter(author_id=author_id)
            if (
                "page" in params and "size" in params
            ):  # make sure param has both page and size in order to paginate
                try:
                    paginator = Paginator(
                        post, int(params["size"]), allow_empty_first_page=True
                    )  # create paginator with size
                    s = PostsSerializer(
                        paginator.page(int(params["page"])), many=True
                    )  # get requested page and serialize
                except (ValueError, EmptyPage, PageNotAnInteger) as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            else:
                s = PostsSerializer(post, context={"request": request}, many=True)
            return Response(s.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        
        try:
            author = Author.objects.get(pk = author_id)
        except Author.DoesNotExist:
            return Response("no author under this id", status=status.HTTP_404_NOT_FOUND)

        try:   
            new_post = Post.objects.create(
            author_id= author,
            title=request.data.get("title",""),
            visibility= request.data.get("visibility", "PU"),
            description= request.data.get("description", ""),
            content= request.data.get("content", ""),
            contentType= request.data.get("contentType", "plain"),
            source = request.data.get("source",""),
            origin = request.data.get("origin",""),
            unlisted = request.data.get("unlisted","False"),
            categories = request.data.get("categories",""),
            count = request.data.get("count","0"),
            )
            new_post.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
