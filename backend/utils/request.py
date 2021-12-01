import enum
from typing import  Tuple, Union
import requests
from requests.exceptions import RequestException
from django.core.cache import cache


from rest_framework.response import Response

from author.models import Author
from posts.models import Post
from comment.models import Comment


from urllib.parse import urlparse


from nodes.models import Node
import base64

def makeRequest(method: str, url: str, data: Union[dict, None] =None) -> Tuple :
    
    # if (method, url) in cache: #if the request has recently been gotten, just return the cached version
    #     return cache.get((method, url))

    parsed = urlparse(url)
    print(parsed)
    if not parsed.scheme or ( parsed.scheme != 'http' and parsed.scheme != 'https'):
        print( ({"error": "invalid url"}, 400))
        return ({"error": "invalid url"}, 400)
        

    #. TODO varifying netloc is pointless :?
    # if not Node.objects.filter(netloc = parsed.netloc).exists():
    #     return Response({"error": "requested domain is not registered"}, status=400)
    
    #node the request is refering to definitely exists
    node : Node= Node.objects.get(netloc = parsed.netloc)
    
    if not node.allowOutgoing:
        print(({"error": "outgoing request to this node is blocked by admin"}, 400)
    )
        return ({"error": "outgoing request to this node is blocked by admin"}, 400)
    
    fixedurl = f"{node.url}{url[url.find('author'):]}"


    try:
        s = f"{node.outgoingName}:{node.outgoingPassword}".encode('utf-8')
        result = requests.request(method, fixedurl,  data=data, headers=({"Authorization": f"Basic {base64.b64encode(s).decode('utf-8')}"} if node.authRequiredOutgoing else {}))
    except RequestException as e:
        print("execption occured in utils.request", str(e))
        return (str(e), 400)
        
    

    response = (result.content, result.status_code)

    # if result.status_code == 200:
    #     cache.set((method, url), response)
    return response




class ClassType(enum.Enum):
    author = 0
    post = 1
    comment = 2

class IsLocalResponse:
    
    def __init__(self, isLocal:bool, type : ClassType, id :str, longId:str):
        self.isLocal = isLocal
        self.type = type
        self.id = id #just <postid>
        self.longId = longId #http://domain.com/authors/<id>/posts/<postid>



def checkIsLocal(fullId:str, type : ClassType = None) -> IsLocalResponse:
    
    '''
    fullid can be either a short or long id, but if using short id, type must be specified
    
    returns a IsLocalResponse object
    '''
    
    shortId = None
    items = fullId.split('/') 
    
    if len(items) > 1:
        try:
            if 'comments' in items:
                shortId = items[items.index('comments') + 1]
                type = ClassType.comment
            elif 'posts' in items:
                shortId = items[items.index('posts') + 1]
                type = ClassType.post
            elif 'author' in items:
                shortId =  items[items.index('author') + 1]
                type = ClassType.author
            else:
                return None
            
        except Exception as e:
            print("error occured converting types in uti.request.checkislocal", e)
            return None
    elif type is None:
        print("type is None and only short id is provided in utils.request.checkIsLocal")
        return None 


    # if has isolate id of the item, and know the type of the item, then just lookup in the respective table to chech for existance.
    isLocal = {ClassType.author: Author, ClassType.post: Post, ClassType.comment: Comment}[type].objects.filter(pk = (shortId if len(items) > 2 else fullId)).exists()
    
    return IsLocalResponse(isLocal, type, shortId if len(items) > 1 else fullId, fullId) 
