import base64
import enum
import json
import threading
import time
import urllib.parse as parse
from dataclasses import dataclass
from typing import List, Tuple, Union
from urllib.parse import urlparse

import requests
from author.models import Author
from backend.settings import NETLOC
from comment.models import Comment
from django.core.cache import cache
from django.http import HttpRequest
from nodes.models import Node
from posts.models import Post
from requests.exceptions import RequestException
from rest_framework.request import Request
from rest_framework.response import Response


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
                # this method dont need parsing
                return func(request, *args, **kwargs)

            url = request.get_full_path()
            parsedId = getId(url, type).replace("~", "/")
            target = f"https://{parsedId}"  # link id has / replaced with - to make them url safe
           
            parsed = parse.urlparse(target)

          
            if parsed.netloc == "" or parsed.path == "":
                parsedRequest = ParsedRequest(
                    request, islocal=True, id=parsedId
                )  # the id provided dont seem like a valid url, treat as normal id instead. good luck.
                return func(parsedRequest, *args, **kwargs)

            if parsed.netloc == NETLOC:
                # the netloc found is our domain, parse for real id.
                parsedId = getId(parsedId, type)
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


@dataclass
class QueryResponse:
    content: str
    status_code: int


def makeRequest(method: str, url: str, data: Union[dict, None] = None) -> QueryResponse:

    cacheKey = f"{method}_{url}"

    if cacheKey in cache:  # if the request has recently been gotten, just return the cached version
        return cache.get(cacheKey)

    parsed = urlparse(url)
    if not parsed.scheme or (parsed.scheme != "http" and parsed.scheme != "https"):

        return QueryResponse("error, invalid url", 400)

    # . TODO varifying netloc is pointless :?
    # if not Node.objects.filter(netloc = parsed.netloc).exists():
    #     return Response({"error": "requested domain is not registered"}, status=400)

    # node the request is refering to definitely exists
    node: Node = Node.objects.get(netloc=parsed.netloc)

    if not node.allowOutgoing:
        return QueryResponse("error, outgoing request to this node is blocked by admin", 400)

    fixedurl = f"{node.url}{url[url.find('author'):]}" 
    if fixedurl[-1] != "/":
        fixedurl += "/"

    try:
        s = f"{node.outgoingName}:{node.outgoingPassword}".encode("utf-8")
        result = requests.request(
            method,
            fixedurl,
            data=json.dumps(data) if type(data) is dict else data,
            headers=({"Authorization": f"Basic {base64.b64encode(s).decode('utf-8')}", "Accept": "*/*", "Content-Type": "application/json"}),
        )
    except RequestException as e:
        print("execption occured in utils.request", str(e))
        return QueryResponse(f"error {str(e)}", 400)

    response = QueryResponse(result.content, result.status_code)

    if 200<=result.status_code < 300:
        cache.set(cacheKey, response)
        
    return response


@dataclass
class IsLocalResponse:

    isLocal: bool
    type: ClassType
    id: str  # just <postid>
    long: str  # http://domain.com/authors/<id>/posts/<postid>


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
    isLocal = {ClassType.AUTHOR: Author, ClassType.POST: Post, ClassType.COMMENT: Comment}[type].objects.filter(pk=(fullId)).exists()

    return IsLocalResponse(isLocal or len(items) < 2, type, shortId if len(items) > 1 else fullId, fullId)


def returnGETRequest(url: str) -> Response:

    if url is None:
        return Response("The requested address is not registered with this server yet.", status=404)

    result = makeRequest("GET", url)
    if 200 <= result.status_code < 300:
        return Response(json.loads(result.content), status=200)
    else:
        return Response("foreign content not found, or some error occured.")


def returnPOSTRequest(url: str, data: Union[str, dict]) -> Response:

    if url is None:
        return Response("The requested address is not registered with this server yet.", status=404)

    result = makeRequest("POST", url, data if type(data) is str else json.dumps(data))

    if 200 <= result.status_code < 300:
        return Response(json.loads(result.content), status=200)
    else:
        return Response("foreign content not found, or some error occured.")


def makeMultipleGETs(
    urls: List[str],
) -> List[Tuple[str, QueryResponse]]:

    output = []
    threads = []
    t0 = time.time()
    for url in urls:
        t = threading.Thread(target=lambda link: output.append((link, makeRequest("GET", link))), args=(url,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print(f"makeMultipleGETs fetched {len(output)} urls, taking {time.time() - t0} ms")

    return output
