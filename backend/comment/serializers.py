

from .models import Comment, Content_choices
from rest_framework import serializers
from author.serializers import AuthorSerializer
from backend.settings import SITE_ADDRESS


class CommentSerializer(serializers.Serializer):
    """
    Serializer for comment model
    """
    type = serializers.SerializerMethodField()
    
    author = AuthorSerializer(read_only=True, many = False)
    
    comment = serializers.CharField(max_length=500)
    
    contentType = serializers.ChoiceField(choices=Content_choices)
    
    published = serializers.DateTimeField(read_only=True)
    
    id = serializers.SerializerMethodField()
    
    class Meta:
        fields = ('type', 'author', 'comment', 'contentType', 'published', 'id')
        ordering = ['published']
    
    def get_id(self, obj: Comment):
        return f"{SITE_ADDRESS}/author/{obj.author.id}/post/{obj.post.id}/{obj.id}"
    
    def get_type(self, obj: Comment):
        return 'comment'