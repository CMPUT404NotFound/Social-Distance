
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

from .models import posts
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@api_view(["GET","POST"])
def getAllPosts(request: Request, author_id):
    """
    GET to get a list of all authors, with pagination options
    POST to register a new author
    """
    if request.method == "GET":
        try:
            
            post = posts.objects.get(pk = author_id).all()
            s = PostsSerializer(post, context={'request': request}, many=True)
            return Response(s.data)
        except posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        pass