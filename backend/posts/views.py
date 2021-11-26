from os import stat
from django.utils.functional import empty
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Empty, Request
from rest_framework.decorators import (
    api_view,
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


@api_view(["GET","POST","DELETE","PUT"])
def managePost(request: Request, author_id, post_id):
    try:
        author = Author.objects.get(pk = author_id)
    except Author.DoesNotExist:
        return Response("no author under this id", status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        try:
            post = Post.objects.get(author_id, post_id)
        except: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = PostsSerializer(post,context={"request": request}, many=True)
        return Response(s.data, status=status.HTTP_200_OK)


    pass
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
            published = request.data.get("published",""),
            categories = request.data.get("categories",""),
            count = request.data.get("count","0"),
            comments = request.data.get("comments","")
            )
            new_post.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
