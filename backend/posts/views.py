
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

from .models import Post
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@swagger_auto_schema(method="get",tags=['posts'])
@swagger_auto_schema(method="post",tags=['posts'])
@api_view(["GET","POST"])
def getAllPosts(request: Request, author_id):
    if request.method == "GET":
        try:
            
            post = Post.objects.get(pk = author_id).all()
            s = PostsSerializer(post, context={'request': request}, many=True)
            return Response(s.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        pass