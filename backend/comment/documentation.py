from drf_yasg import openapi
from drf_yasg.inspectors.base import FieldInspector
from rest_framework import serializers
from .serializers import CommentSerializer


class NoSchemaTitleInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        # remove the `title` attribute of all Schema objects
        if isinstance(result, openapi.Schema.OR_REF):
            # traverse any references and alter the Schema object in place
            schema = openapi.resolve_ref(result, self.components)
            schema.pop("title", None)
            if schema.get("minLength", 0) == 1:
                schema.pop("minLength", None)

            # no ``return schema`` here, because it would mean we always generate
            # an inline `object` instead of a definition reference

        # return back the same object that we got - i.e. a reference if we got a reference
        return result


class GetCommentsSerializer(serializers.Serializer):

    type = serializers.SerializerMethodField()
    page = serializers.IntegerField(default=1, min_value=1)
    size = serializers.IntegerField(default=1, min_value=1)
    post = serializers.URLField()
    id = serializers.URLField()
    comments = CommentSerializer(many=True)

    def get_type(self, obj):
        return "comments"


getCommentsResponse = openapi.Response("A comments of a post", GetCommentsSerializer)
