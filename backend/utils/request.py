import enum
from typing import Literal, Tuple, Union
import requests
from requests.exceptions import RequestException
from django.core.cache import cache

from rest_framework.response import Response

from author.models import Author
from posts.models import Post
from comment.models import Comment

def makeRequest(method: str, url: str, data: Union[dict, None] =None):
    if (method, url) in cache:
        return cache.get((method, url))

    try:
        result = requests.request(method, url, data=data)
    except RequestException as e:
        result = requests.Response(str(e))
        print("execption occured in utils.request", str(e))
    
    response = Response(result.content, result.status_code)

    if response.status_code == 200:
        cache.set((method, url), response)
    return response





class ClassType(enum.Enum):
    author = 0
    post = 1
    comment = 2

def checkIsLocal(id:str, type = None) -> Tuple[str, str]:
    '''
    returns (type, id) if is local, None otherwise. 
    Type is stuff like author, posts, comments, etc
    
    the type param should be provided if id is just a uuid, 
    otherwise id should be a link
    '''
    if not type:
        items = id.split('/')
        try:
            if 'comments' in items:
                id = items[items.index('comments') + 1]
                type = ClassType.comment
            elif 'posts' in items:
                id = items[items.index('posts') + 1]
                type = ClassType.post
            elif 'author' in items:
                id =  items[items.index('author') + 1]
                type = ClassType.author
            else:
                return None
            
        except Exception as e:
            print("error occured converting types in uti.request.checkislocal", e)


    # if has isolate id of the item, and know the type of the item, then just lookup in the respective table to chech for existance.
    return (id, type) if {0: Author, 1: Post, 2: Comment}[type].objects.filter(pk = id).exists() else None
    
