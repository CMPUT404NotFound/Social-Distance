from os import stat
from typing import Union
from django.contrib.auth import authenticate
from django.http.request import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import (
    api_view,
    authentication_classes,
)
from rest_framework import status




from .token import TokenAuth, expires_in, refreshToken, NodeBasicAuth

from .models import Author
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .documentations import *

from django.db.utils import IntegrityError
import django.utils.timezone as timezone
from globalSetting.models import Setting

from utils.request import parseIncomingRequest, ParsedRequest, ClassType, makeRequest
import json

from Followers.models import Follower
from posts.models import Post
from comment.models import Comment
from likes.models import Like
# Create your views here.


@swagger_auto_schema(
    method="get",
    operation_summary="Get a single author by id in path",
    responses={200: getAuthorResponse, 404: "Author not found"},
    field_inspectors=[NoSchemaTitleInspector],
    tags=["Author"],
)
@swagger_auto_schema(
    method="post",
    operation_summary="Update an author's information. (id requried in body for authentication)(do not include field that doesn't need to be updated.)",
    responses={204: "update success", 404: "Author not found"},
    field_inspectors=[NoSchemaTitleInspector],
    request_body=AuthorUpdateSerializer,
    # manual_parameters=[
    #     openapi.Parameter(
    #         name="Authorization",
    #         in_=openapi.IN_HEADER,
    #         type=openapi.TYPE_STRING,
    #         description="Authorization token",
    #         default="Token <token>",
    #     )
    # ],
    tags=["Author"],
)
@api_view(["GET", "POST"])
@authentication_classes([TokenAuth(needAuthorCheck=["POST"]), NodeBasicAuth])
@parseIncomingRequest(methodToCheck=["GET"], type=ClassType.AUTHOR)
def handleAuthorById(request: Union[ParsedRequest, HttpRequest], authorId):
    
    if request.method == "GET":
        if request.islocal:
            try:
                author = Author.objects.get(pk=request.id)

                s = AuthorSerializer(author)
                return Response(s.data, status=200)

            except Author.DoesNotExist:

                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if request.id is None:
                return Response("The requested address is not registered with this server yet.", status=404)
            
            result = makeRequest("GET", request.id)
            if 200 <= result.status_code < 300:  # TIL chain comparison exist in python
                return Response(json.loads(result.content), status=200)
            else:
                return Response("foreign content not found, or some error occured while fetching it", status=404)

    elif request.method == "POST":
        """
        Author Updates, auth needed
        """
        try:
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
    tags=["Author"],
)
@api_view(["GET"])
def getAllAuthors(request: Request):
    """
    GET to get a list of all authors, with pagination options\n
    """
    # TODO add ordering to authors
    if request.method == "GET":
        # danger zone!
        # from random import randint
        # for author1 in Author.objects.all():
        #     for author2 in Author.objects.all():
        #         if randint(0, 2) == 1:
        #             Follower.objects.create(sender = author1.id, receiver = author2)
        
        # import lorem
        # from random import randint
        # for author in Author.objects.all():
            
        #     for i in range(6):
        #         if randint(0, 3) == 1:
        #             Post.objects.create(author_id = author,
        #                                 title = lorem.sentence(),
        #                                 description = lorem.sentence(),
        #                                 content = lorem.paragraph(),
        #                                 source = SITE_ADDRESS,
        #                                 origin = SITE_ADDRESS,
        #                                 )
        
        # for post in Post.objects.all():
        #     for i in range(3):
        #         if randint(0 ,2) == 1:
        #             Comment.objects.create(post = post, author = post.author_id.id, comment = lorem.sentence())
        
        # for author in Author.objects.all():
        #     for post in Post.objects.all():
        #         if randint(0, 4) == 1:
        #             Like.objects.create(author = author.id, parentId = post.pk)
        #     for comment in Comment.objects.all():
        #         if randint(0, 4) == 1:
        #             Like.objects.create(author = author.id, parentId = comment.pk)
        params: dict = request.query_params

        authors = Author.objects.all()
        if "page" in params and "size" in params:  # make sure param has both page and size in order to paginate
            try:
                paginator = Paginator(authors, int(params["size"]), allow_empty_first_page=True)  # create paginator with size
                s = AuthorSerializer(paginator.page(int(params["page"])), many=True)  # get requested page and serialize
            except (ValueError, EmptyPage, PageNotAnInteger) as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        else:
            s = AuthorSerializer(authors, many=True)
        return Response(s.data)


def returnToken(user: Author):
    token, created = Token.objects.get_or_create(user=user)

    if not created:
        token = refreshToken(token)

    user.last_login = timezone.now()
    user.save()

    return {
        "token": token.key,
        "expires_in": expires_in(token),
        "author": AuthorSerializer(user).data,
    }


@swagger_auto_schema(
    method="post",
    operation_summary="Sign up with username and password. author personal info optional",
    responses={
        201: "author created",
        204: "author created, but need server admin to activate in order to login.",
        400: "bad sign up information",
        409: "username already exist",
    },
    field_inspectors=[NoSchemaTitleInspector],
    request_body=SignUpSerializer,
    tags=["Authentications"],
)
@api_view(["POST"])
@authentication_classes([TokenAuth(bypassEntirely=["POST"])])
def signUp(request: Request):
    data = request.data
    try:

        setting: Setting = Setting.settings()

        user = Author.objects.create_user(
            data["userName"],
            data.get("displayName", data["userName"]),
            data.get("github", ""),
            data.get("profileImage", ""),
            data["password"],
            is_active=not setting.newUserRequireActivation,
        )
        if setting.newUserRequireActivation:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # successful account creation, return login token

        return Response(returnToken(user), status=status.HTTP_201_CREATED)
    except (ValueError, AttributeError) as error:
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as error:
        return Response(str(error), status=status.HTTP_409_CONFLICT)


@swagger_auto_schema(
    method="post",
    operation_summary="login with username and password, returns a token for future authentications",
    responses={
        200: openapi.Response("Successful login, with author info and token", LoginSuccessSerializer),
        400: "bad login request format",
        401: "Invalid login credentials",
        403: "Account not yet activated by admin",
    },
    field_inspectors=[NoSchemaTitleInspector],
    request_body=LoginSerializer,
    tags=["Authentications"],
)
@api_view(["POST"])
@authentication_classes([TokenAuth(bypassEntirely=["POST"])])
def login(request: Request) -> Response:

    """
    handles login request
    """
    s = LoginSerializer(data=request.data)

    if not s.is_valid():
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=s.data["userName"], password=s.data["password"])

    if not user:
        return Response(
            {"error": "Invalid login info."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if not user.is_active:
        return Response({"error": "this account has not yet been activated by the admin"}, status=status.HTTP_403_FORBIDDEN)

    return Response(returnToken(user), status=200)


@swagger_auto_schema(
    method="post",
    operation_summary="if the request token matches author id, logout this user/delete the user's token",
    responses={
        200: "logout success",
        401: "token mismatch or not provided, or some other auth related error."
    },
    tags=["Authentications"]
)
@api_view(["POST"])
@authentication_classes([TokenAuth(needAuthorCheck=["POST"])])
def logout(request: Union[Request, HttpRequest]):
    
    #author identity is already checked, just logout is safe
    
    Token.objects.filter(user = request.user).delete()
    
    return Response("logging out aka delete token success.", status=200)
        


# todo make logout api


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
