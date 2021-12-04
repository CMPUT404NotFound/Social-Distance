import base64
import binascii
import datetime
from typing import List, Union


import backend.settings as settings
from rest_framework.authentication import TokenAuthentication, get_authorization_header, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
import django.utils.timezone as timezone
from .models import Author
from rest_framework import exceptions

from django.http.request import HttpRequest
from rest_framework.request import Request

from nodes.models import Node

def expires_in(token: Token) -> int:
    """
    Check remining time until token expires in seconds
    returns 0 if token is expired already.
    """
    return max(
        datetime.timedelta(0),
        (token.created + datetime.timedelta(0, settings.TOKEN_EXPIRE_TIME, 0)) - timezone.now(),
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


class DummyAuthObject:
    def __init__(self, user=False, is_authenticated = False):
        self.user = user
        self.is_authenticated = is_authenticated

class TokenAuth(TokenAuthentication):
    """
    Every request from front end must provide token, (unless for login to obtain token)
    token is needed to verify the requester is the our own frontend.
    it's optional to require some methods to have the same author as well.

    This authenticator always fails for foreign requests since they can't provide token.
    * TODO write NodeBasicAuth to take over if TokenAuth fails.
    * TODO let admin activate/deactivate author
    """

    def __init__(self, needAuthorCheck: List[str] = None, bypassEntirely: List[str] = None):
        
        self.needAuthorCheck = needAuthorCheck if needAuthorCheck else []
        self.bypassEntirely = bypassEntirely if bypassEntirely else []

    def __call__(self):
        return self  # a bit of a hack, to allow initial tokenAuth with initialized params

    def authenticate(self, request):
        """
        mostly code ripped from the super class

        Ensures that request has a valid token
        """
        
        print("startting token auth")
        if request.method in self.bypassEntirely:
            return (DummyAuthObject(True, True),None)

        auth = get_authorization_header(request).split()
        print(auth, not auth , (auth[0].lower() != "token".lower().encode() and auth[0].lower() != "bearer".encode()))
        
        if not auth or (auth[0].lower() != "token".lower().encode() and auth[0].lower() != "bearer".encode()):
            print("returning none!")
            return None #when None is returned, the request is passed to the next auth class
        
        if not auth or len(auth) == 1:
            raise AuthenticationFailed("Invalid token header. No credentials provided.")
        elif len(auth) > 2:
            raise AuthenticationFailed("Invalid token header. Token string should not contain spaces.")
        
        try:
            token = Token.objects.get(pk=auth[1].decode())
        except UnicodeError:
            raise AuthenticationFailed("Invalid token header. Token string should not contain invalid characters.")
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")
        

        try:
            author2: Author = Token.objects.get(key=token).user
        except Token.DoesNotExist as e:
            raise AuthenticationFailed("Token does not belong to any user")

        if author2.is_admin:
            return (author2, token)  # if token provided belongs to admin, no need to check if the users matchs, nor if the token is expired.

        if  request.method in self.needAuthorCheck:
            try:
                id = (items := request.path.split("/"))[items.index("author") + 1]

                author1 = Author.objects.get(pk=id)  # if there is no id in the request, then force NotFound Exception
            except Author.DoesNotExist:
                #: FIXME this is not a good way to verify if token author and requested author matches, maybe?
                raise AuthenticationFailed("Author not found. Is id included in the request? If so, a Author with corresponding id is not found.")

            if author1 != author2:  # if the token belongs to admin, then user identity check can be skipped
                raise AuthenticationFailed("Token's Author and Request's author does not match")

        if token_expired(token):
            raise AuthenticationFailed("Token expired")

        return (token.user, token)




class NodeBasicAuth(BasicAuthentication):
    
    def __init__(self, blockedMethod: List[str] = None):
        
        self.blockedMethod = blockedMethod if blockedMethod else []


    def __call__(self):
        return self  # a bit of a hack, to allow initial tokenAuth with initialized params
    
    def authenticate(self, request: Union[Request, HttpRequest]):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        
        print("startting basic auth")
        auth = get_authorization_header(request).split()

        if request.method in self.blockedMethod:
            raise exceptions.AuthenticationFailed("external access of this api call is not allowed.")

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = 'Invalid basic header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid basic header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)


        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode('latin-1')
            auth_parts = auth_decoded.partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = 'Invalid basic header. Credentials not correctly base64 encoded.'
            raise exceptions.AuthenticationFailed(msg)

        username, password = auth_parts[0], auth_parts[2]
        
        #origin not needed anymore
        # try: 
        #     #origin is used to later varify if this requester is trusted
        #     origin = request.headers['Origin']
        # except KeyError:
        #     raise exceptions.AuthenticationFailed("Origin header not provided")
    
        try:
            node : Node= Node.objects.get(incomingName = username)
            
            if not node.allowIncoming:
                raise exceptions.AuthenticationFailed("The origin provided is not allowed to access this server")

            
            
            if not node.incomingPassword == password:
                raise exceptions.AuthenticationFailed("Basic auth credentials does not match.")
                
        except Node.DoesNotExist:
            raise exceptions.AuthenticationFailed("The origin provided is not yet registered in this server")
        
        return (DummyAuthObject(True, True), None)
      
        
        