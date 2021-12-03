import enum
from typing import List, Tuple, Union
import requests
from requests.exceptions import RequestException
from django.core.cache import cache


from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from author.models import Author
from posts.models import Post
from comment.models import Comment
from urllib.parse import urlparse
from backend.settings import NETLOC

from nodes.models import Node
import base64

import urllib.parse as parse


class ClassType(enum.Enum):
    AUTHOR = 0
    POST = 1
    COMMENT = 2


class ParsedRequest(Request):
    def __init__(self, request: Request, islocal: bool, id: str):

        self.__dict__ = request.__dict__  # inherit all methods and fields of a instance of Request

        self.id = id
        self.islocal = islocal


def getId(link: str, type: ClassType):
    items = link.split("/")
    if type == ClassType.AUTHOR:
        target = items[items.index("author") + 1]
    elif type == ClassType.POST:
        target = items[items.index("posts") + 1]
    elif type == ClassType.COMMENT:
        target = items[items.index("comments") + 1]
    else:
        raise Exception("unknown class type at getid, util.request")
    return target


def parseIncomingRequest(methodToCheck: List[str] = None, type: ClassType = ClassType.AUTHOR):
    def decorateFunc(func):
        def inner(request: Union[Request, HttpRequest], *args, **kwargs):
            
            if request.method not in methodToCheck:
                #this method dont need parsing
                return func(request, *args, **kwargs)
                
            
            url = request.get_full_path()
            parsedId = getId(url, type).replace("~", "/")
            target = f'https://{parsedId}' # link id has / replaced with - to make them url safe
            print(target)
            parsed = parse.urlparse(target)

            print(parsed, NETLOC)
            if parsed.netloc == "" or parsed.path == "":
                parsedRequest = ParsedRequest(
                    request, islocal=True, id=parsedId
                )  # the id provided dont seem like a valid url, treat as normal id instead. good luck.
                return func(parsedRequest, *args, **kwargs)
                

            if parsed.netloc == NETLOC:
                # the netloc found is our domain, parse for real id.

                
                print("realid", parsedId)
                parsedRequest = ParsedRequest(request, islocal=True, id=parsedId)  # is local is true and id is author id provided by frontend
                return func(parsedRequest, *args, **kwargs)
                

            # now we know the netloc is neither blank nor our domain, lets check if we have the domain in our nodes db

            if not Node.objects.filter(netloc=parsed.netloc).exists():
                # the domain requested is not registered
                return func(ParsedRequest(request, islocal=False, id=None), *args, **kwargs)

            if target[-1] != "/":
                target += "/"
            parsedRequest = ParsedRequest(request, islocal=False, id=target)
            return func(parsedRequest, *args, **kwargs)

        return inner

    return decorateFunc


def makeRequest(method: str, url: str, data: Union[dict, None] = None) -> Tuple:

    cacheKey = str((method, url))

    if cacheKey in cache:  # if the request has recently been gotten, just return the cached version
        return cache.get(cacheKey)

    parsed = urlparse(url)
    if not parsed.scheme or (parsed.scheme != "http" and parsed.scheme != "https"):
        print(({"error": "invalid url"}, 400))
        return ({"error": "invalid url"}, 400)

    # . TODO varifying netloc is pointless :?
    # if not Node.objects.filter(netloc = parsed.netloc).exists():
    #     return Response({"error": "requested domain is not registered"}, status=400)

    # node the request is refering to definitely exists
    node: Node = Node.objects.get(netloc=parsed.netloc)

    if not node.allowOutgoing:
        print(({"error": "outgoing request to this node is blocked by admin"}, 400))
        return ({"error": "outgoing request to this node is blocked by admin"}, 400)

    fixedurl = f"{node.url}{url[url.find('author'):]}"

    try:
        s = f"{node.outgoingName}:{node.outgoingPassword}".encode("utf-8")
        result = requests.request(
            method,
            fixedurl,
            data=data,
            headers=({"Authorization": f"Basic {base64.b64encode(s).decode('utf-8')}"} if node.authRequiredOutgoing else {}),
        )
    except RequestException as e:
        print("execption occured in utils.request", str(e))
        return (str(e), 400)

    response = (result.content, result.status_code)

    if result.status_code == 200:
        cache.set(cacheKey, response)
    return response


class IsLocalResponse:
    def __init__(self, isLocal: bool, type: ClassType, id: str, longId: str):
        self.isLocal = isLocal
        self.type = type
        self.id = id  # just <postid>
        self.longId = longId  # http://domain.com/authors/<id>/posts/<postid>


def checkIsLocal(fullId: str, type: ClassType = None) -> IsLocalResponse:

    """
    fullid can be either a short or long id, but if using short id, type must be specified

    returns a IsLocalResponse object
    """

    shortId = None
    items = fullId.split("/")

    if len(items) > 1:
        try:
            if "comments" in items:
                shortId = items[items.index("comments") + 1]
                type = ClassType.COMMENT
            elif "posts" in items:
                shortId = items[items.index("posts") + 1]
                type = ClassType.POST
            elif "author" in items:
                shortId = items[items.index("author") + 1]
                type = ClassType.AUTHOR
            else:
                return None

        except Exception as e:
            print("error occured converting types in uti.request.checkislocal", e)
            return None
    elif type is None:
        print("type is None and only short id is provided in utils.request.checkIsLocal")
        return None

    # if has isolate id of the item, and know the type of the item, then just lookup in the respective table to chech for existance.
    isLocal = (
        {ClassType.AUTHOR: Author, ClassType.POST: Post, ClassType.COMMENT: Comment}[type]
        .objects.filter(pk=(shortId if len(items) > 2 else fullId))
        .exists()
    )

    return IsLocalResponse(isLocal, type, shortId if len(items) > 1 else fullId, fullId)
