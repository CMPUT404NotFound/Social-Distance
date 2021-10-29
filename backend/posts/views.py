from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from author.models import Author
from .models import posts
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@swagger_auto_schema(method="get",tags=['posts'])
@swagger_auto_schema(method="post",tags=['posts'])
@api_view(["GET","POST"])
def getAllPosts(request: Request, author_id):
    if request.method == "GET":
        try:
            post = posts.objects.filter(author_id=author_id)
            s = PostsSerializer(post, context={"request": request}, many=True)
            return Response(s.data)
        except posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        try:
            author = Author.objects.get(pk = author_id)

            new_post = posts.objects.create(
               author_id= author,
               title=request.data['title'],
               visibility= request.data['visibility'],
            )
            # author.sender.add(follower)
            new_post.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
