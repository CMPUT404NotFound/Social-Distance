
from drf_yasg.inspectors import FieldInspector
from drf_yasg import openapi
from rest_framework import serializers

from .serializers import AuthorSerializer

getAuthorResponse = openapi.Response(
    "A single author with corresponding id", AuthorSerializer
)


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


class AuthorUpdateSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    github = serializers.URLField(required=False)
    displayName = serializers.CharField(required=False)
    profileImage = serializers.URLField(required=False)

    class Meta:
        ref_name = None


class SignUpSerializer(serializers.Serializer):
    userName = serializers.CharField(required=True, max_length=40)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    github = serializers.URLField(required=False)
    displayName = serializers.CharField(required=False)
    profileImage = serializers.URLField(required=False)

    class Meta:
        ref_name = None


class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField(required=True, max_length=40)
    password = serializers.CharField(
        required=True,
    )

    class Meta:
        ref_name = None


class LoginSuccessSerializer(serializers.Serializer):
    token = serializers.CharField()
    expires_in = serializers.FloatField()
    user = AuthorSerializer()

    class Meta:
        ref_name = None
