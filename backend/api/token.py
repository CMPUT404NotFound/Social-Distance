import datetime

from pytz import utc

import backend.settings as settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import django.utils.timezone as timezone


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
    def authenticate_credentials(self, key):

    
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            # token given is not found in database
            print("not found")
            raise AuthenticationFailed("Invalid token")

        if token_expired(token):
            raise AuthenticationFailed("Token expired")

        token = refreshToken(token)  # if authentication is successful, refresh token

        return (token.user, token)
