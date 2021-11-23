import datetime
from typing import List

import uuid

import backend.settings as settings
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import django.utils.timezone as timezone
from .models import Author


def expires_in(token: Token) -> int:
    """
    Check remining time until token expires in seconds
    returns 0 if token is expired already.
    """
    return max(
        datetime.timedelta(0),
        (token.created + datetime.timedelta(0, settings.TOKEN_EXPIRE_TIME, 0))
        - timezone.now(),
    )


def token_expired(token: Token) -> bool:
    return expires_in(token) == datetime.timedelta(0)


def refreshToken(token: Token) -> Token:
    """
    Check if token is expired and if it is, delete it.
    Then return a new token
    """
    if token_expired(token):
        token.delete()
        token = Token.objects.create(user=token.user)
    return token


class TokenAuth(TokenAuthentication):
    
    def __init__(self, bypassedMethod : List[str]):
        self.bypassed = bypassedMethod
    
    def __call__(self):
        return self #a bit of a hack, to allow initial tokenAuth with initialized params
    
    def authenticate(self, request):
        """
        mostly code ripped from the super class

        Ensures that request has a valid token
        """

        if request.method in self.bypassed:
            return ("", None)
        
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise AuthenticationFailed("Invalid token header. No credentials provided.")
        elif len(auth) > 2:
            raise AuthenticationFailed(
                "Invalid token header. Token string should not contain spaces."
            )

        try:
            token = Token.objects.get(pk=auth[1].decode())
        except UnicodeError:
            raise AuthenticationFailed(
                "Invalid token header. Token string should not contain invalid characters."
            )

        try:
            author2 = Token.objects.get(key=token).user
        except Token.DoesNotExist as e:
            raise AuthenticationFailed("Invalid token")

        try:
            id = (items := request.path.split("/"))[items.index("author") + 1]

            author1 = Author.objects.get(
                pk=id
            )  # if there is no id in the request, then force NotFound Exception
        except Author.DoesNotExist:
            raise AuthenticationFailed(
                "Author not found. Is id included in the request? If so, a Athor with corresponding id is not found."
            )

        if (
            author1 != author2 and not author1.is_admin
        ):  # if the token belongs to admin, then user identity check can be skipped
            raise AuthenticationFailed(
                "Token's Author and Request's author does not match"
            )

        if token_expired(token):
            raise AuthenticationFailed("Token expired")

        return (token.user, token)
