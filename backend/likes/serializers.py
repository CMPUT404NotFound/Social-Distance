from rest_framework import serializers
from .models import Like
from backend.settings import SITE_ADDRESS




class LikeSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Like
        fields = ('type', 'author',   "object")
    
    type = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    
    def get_type(self, obj):
        return 'Like'
    
    def get_object(self, obj):
        return obj.parentId
    
    def to_representation(self, obj):
        repr = super().to_representation(obj)
        repr['@context'] = "https://www.w3.org/ns/activitystreams"
        return repr