from django.shortcuts import render
from rest_framework.decorators import api_view
from backend.author.models import Author
from backend.likes.models import Like
from backend.likes.serializers import LikeSerializer

from posts.models import Post
from rest_framework.response import Response
# Create your views here.



@api_view(["GET"])
def getPostLikes(request, postId):
    
    
    try: 
        post = Post.objects.get(pk = postId)
    except Post.DoesNotExist:
        return Response("post does not exist", status=404)
    
    likes = Like.objects.filter(parentId = postId)
    
    return Response(LikeSerializer(likes.all(), many = True).data, status=200)


@api_view(["GET"])
def getCommentLikes(request, commentId):
    
    try: 
        comment = Post.objects.get(pk = commentId)
    except Post.DoesNotExist:
        return Response("comment does not exist", status=404)
    
    likes = Like.objects.filter(parentId = commentId)
    
    return Response(LikeSerializer(likes.all(), many = True).data, status=200)

@api_view(['GET'])
def getLiked(request, authorId):
    
    try: 
        author = Author.objects.get(pk=authorId)
    except Author.DoesNotExist:
        return Response("author does not exist", status= 404)
    
    likes = Like.objects.filter(author = authorId).all()
    
    return Response({
            "type": "liked",
            "items": LikeSerializer(likes, many = True).data
        }, status=200)