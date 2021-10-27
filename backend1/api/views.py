from os import name
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from api.token import expires_in, refreshToken


from .models import Author
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.documentation import *
from drf_yasg.utils import swagger_auto_schema


# Create your views here.


@swagger_auto_schema(
    method="get",
    operation_summary="Get a single author by id in path",
    responses={200: getAuthorResponse, 404: "Author not found"},
    field_inspectors=[NoSchemaTitleInspector],
)
@swagger_auto_schema(
    method="post",
    operation_summary="Update an author's information. (id requried in body for authentication)(do not include field that doesn't need to be updated.)",
    responses={204: "update success", 404: "Author not found"},
    field_inspectors=[NoSchemaTitleInspector],
    request_body=AuthorUpdateSerializer,
    manual_parameters=[
        openapi.Parameter(
            name="Authorization",
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description="Authorization token",
            default="Token <token>",
        )
    ],
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def handleAuthorById(request: Request, id):
    if request.method == "GET":
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
            a.displayName = data.get("displayName", a.displayName)
            a.github = data.get("github", a.github)
            a.profileImage = data.get("profileImage", a.profileImage)
            a.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except (Author.DoesNotExist, Token.DoesNotExist) as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="get",
    operation_summary="Get all authors in this server. With optional pagination query params",
    responses={200: getAuthorResponse, 404: "bad pagination"},
    field_inspectors=[NoSchemaTitleInspector],
    manual_parameters=[
        openapi.Parameter(
            name="page",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Page number",
            default=1,
        ),
        openapi.Parameter(
            name="size",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Page size",
            default=10,
        ),
    ],
)
@api_view(["GET"])
def getAllAuthors(request: Request):
    """
    GET to get a list of all authors, with pagination options\n
    """
    # TODO add ordering to authors
    if request.method == "GET":
        params: dict = request.query_params

        authors = Author.objects.all()
        if (
            "page" in params and "size" in params
        ):  # make sure param has both page and size in order to paginate
            try:
                paginator = Paginator(
                    authors, int(params["size"]), allow_empty_first_page=True
                )  # create paginator with size
                s = AuthorSerializer(
                    paginator.page(int(params["page"])), many=True
                )  # get requested page and serialize
            except (ValueError, EmptyPage, PageNotAnInteger) as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        else:
            s = AuthorSerializer(authors, many=True)
        return Response(s.data)


@swagger_auto_schema(
    method="post",
    operation_summary="Sign up with username and password. author personal info optional",
    responses={201: "author created", 400: "bad sign up information"},
    field_inspectors=[NoSchemaTitleInspector],
    request_body=SignUpSerializer,
)
@api_view(["POST"])
def signUp(request: Request):
    data = request.data
    try:
        Author.objects.create_user(
            data["userName"],
            data.get("displayName", data["userName"]),
            data.get("github", ""),
            data.get("profileImage", ""),
            data["password"],
        )
        return Response(status=status.HTTP_201_CREATED)
    except (ValueError, AttributeError) as error:
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    operation_summary="login with username and password, returns a token for future authentications",
    responses={
        200: openapi.Response(
            "Successful login, with author info and token", LoginSuccessSerializer
        ),
        404: "Invalid login",
        400: "bad login request format",
    },
    field_inspectors=[NoSchemaTitleInspector],
    request_body=LoginSerializer,
)
@api_view(["POST"])
def login(request: Request) -> Response:

    """
    handles login request
    """
    s = LoginSerializer(data=request.data)

    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    print(s.data)
    user = authenticate(username=s.data["userName"], password=s.data["password"])

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
