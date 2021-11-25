
from rest_framework import serializers
from posts.serializers import PostsSerializer
from likes.serializers import LikeSerializer
from Followers.serializers import FollowerSerializer


#todo custom serializer needed
class InboxItemSerializer(serializers.Serializer):
    
    
    post = PostsSerializer()
    like = LikeSerializer()
    follow_request = FollowerSerializer()
    
    
    