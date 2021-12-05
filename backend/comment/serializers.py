from author.models import Author
from .models import Comment, Content_choices
from rest_framework import serializers
from author.serializers import AuthorSerializer
from backend.settings import SITE_ADDRESS

from utils.request import checkIsLocal,ClassType, makeRequest

import json 
# stolen from here https://newbedev.com/django-rest-framework-with-choicefield
class ChoiceField(serializers.ChoiceField):
    
    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class CommentSerializer(serializers.Serializer):
    """
    Serializer for comment model
    """

    type = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()

    comment = serializers.CharField(max_length=500)

    contentType = ChoiceField(choices=Content_choices)

    published = serializers.DateTimeField(read_only=True)

    id = serializers.SerializerMethodField()

    class Meta:
        fields = ("type", "author", "comment", "contentType", "published", "id")
        ordering = ["published"]
    
    def get_author(self, obj : Comment):
    
        data = checkIsLocal(obj.author, ClassType.AUTHOR)
        
        if data.isLocal:
            return AuthorSerializer(Author.objects.get(pk = data.id)).data
        else:
            result = makeRequest("GET", data.longId)
 
            if 200 <=result.status_code < 300:
                return json.loads(result[0])
            else: 
                return AuthorSerializer().data
            

    def get_id(self, obj: Comment):
        data = checkIsLocal(obj.author, ClassType.AUTHOR)
        return f"{SITE_ADDRESS}author/{data.id}/posts/{obj.post.post_id}/comments/{obj.id}"

    def get_type(self, obj: Comment):
        return "comment"


