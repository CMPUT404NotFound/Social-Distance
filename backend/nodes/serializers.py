from rest_framework.serializers import ModelSerializer, Serializer

from nodes.models import Node



class NodeSerializer(ModelSerializer):
    
    class Meta:
        model = Node
        fields = ("url", "allowIncoming", "allowOutgoing", "description")