
from django.core import paginator
from rest_framework.response import Response
from rest_framework.request import Request
# Create your views here.

from rest_framework.decorators import (
    api_view,
)


from .models import Comment, Post
from .serializers import CommentSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET', 'POST'])
def handleComments(request:Request, authorId:str, postId:str):
    
    
    if request.method == 'GET':
        try:
            comments = Post.objects.get(pk = postId).post_comments.all()
        except Post.DoesNotExist:
            return Response("no comments under this post",status=404)
        params :dict = request.query_params
        if ("page" in params and "size" in params):
            try:
                pager = Paginator(comments, int(params["size"]))
                serial = CommentSerializer(pager.page(int(params["page"])), many=True)
            except (ValueError, EmptyPage, PageNotAnInteger) as e:
                return Response(str(e), status=400)
        else:
            serial = CommentSerializer(comments, many=True)
        return Response(serial.data, status=200)
    
    elif request.method == 'POST':
        return Response({'message': 'POST'})