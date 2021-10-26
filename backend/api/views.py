from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from api.token import expires_in, refreshToken
from api.token import TokenAuth

from .models import Author
from .serializers import *

# Create your views here.


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def handleAuthorById(request: Request, id):
    print("entering ")
    if request.method == "GET":
        print("GET")
        try:
            author = Author.objects.get(pk=id)
            s = AuthorSerializer(author)
            return Response(s.data)

        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        """
        Author Updates, auth needed
        """
        print("post")
        try:
            print("test", id)
            a: Author = Author.objects.get(pk=id)
            data = request.data

            if Token.objects.get(key=request.auth).user != a:
                raise Author.DoesNotExist()

            a.displayName = data.get("displayName", a.displayName)
            a.github = data.get("github", a.github)
            a.profileImage = data.get("profileImage", a.profileImage)
            a.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except (Author.DoesNotExist, Token.DoesNotExist) as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def getAllAuthors(request: Request):
    """
    GET to get a list of all authors, with pagination options
    POST to register a new author
    """
    if request.method == "GET":
        # TODO pagination/query params. (if no params given, return 5 most recent)
        authors = Author.objects.all()
        s = AuthorSerializer(authors, many=True)
        return Response(s.data)


@api_view(["POST"])
def signUp(request: Request):
    data = request.data
    try:
        Author.objects.create_user(
            data["displayName"],
            data.get("github", ""),
            data.get("profileImage", ""),
            data["password"],
        )
        return Response(status=status.HTTP_201_CREATED)
    except (ValueError, AttributeError) as error:
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request: Request) -> Response:

    """
    handles login request
    """
    s = LoginSerializer(data=request.data)

    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=s.data["displayName"], password=s.data["password"])

    if not user:
        return Response(
            {"error": "Invalid login info. Or account not activated by server admin"},
            status=status.HTTP_404_NOT_FOUND,
        )

    token, created = Token.objects.get_or_create(user=user)

    if not created:
        token = refreshToken(token)

    return Response(
        {
            "token": token.key,
            "expires_in": expires_in(token),
            "author": AuthorSerializer(user).data,
        },
        status=status.HTTP_200_OK,
    )


"""
{
    "token": "b1b4d2f1ec7aeef9f76f91c4d97269cde1bbacf3",
    "expires_in": "10798.388195",
    "author": {
        "type": "Author",
        "id": "f659e6cb-a75a-4795-bbf7-704d243204ab",
        "displayName": "goldentoaste",
        "host": "temp place holder host name",
        "url": "placeholderserice/author/f659e6cb-a75a-4795-bbf7-704d243204ab",
        "github": "",
        "profileImage": ""
    }
}
"""
