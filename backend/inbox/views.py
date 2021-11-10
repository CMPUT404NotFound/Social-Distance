

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from author.models import Author
from Followers.models import Follow_Request
from comment.models import Comment
from posts.models import Post
from inbox.models import InboxItem
from likes.models import Like

from author.token import TokenAuth
from utils.permission import CustomPermissionFilter

# Create your views here.

def getAuthorId(request, authorId):
    print(request.data.get('author', "xd"))
    authorid = request.data.get('author', None)
    if authorId is None:
        authorid = request.data.get("actor")['id']
    else:
        authorid = authorid['id']
        
    realAuthorId = authorid.split('/author/')[-1]
    
    if Author.objects.filter(pk = realAuthorId).exists():
        return realAuthorId
    return authorid

def handleLike(request, authorId):
    try:
        data = request.data
        authorid = getAuthorId(request, authorId)
        
        try:
            author = Author.objects.get(pk = str(authorId))
        except Author.DoesNotExist:
            return Response('Author does not exist', status= 404)
        
        if 'comment' in data['object']:
            parentId = data['object'].split('/comment/')[-1]
            if not Comment.objects.filter(pk = parentId).exists():
                parentId = None
        elif 'posts' in data['object']:
            parentId = data['object'].split('/posts/')[-1]
            if not Post.objects.filter(pk = parentId).exists():
                parentId = None
        else:
            parentId = None

        if parentId:
            like = Like.objects.create(author = authorid, parentId = parentId, summary = data.get('summary', ""))
            InboxItem.objects.create(author = author, type = 'L', contentId = like.pk )
            return Response(status=201)
        
        return Response("invalid id for comment or post",status=404)

    except KeyError:
        return Response('bad body format', status=400)

def handleFollows(request, authorId: str):
    try:
        follower = getAuthorId(request, authorId)
        
        try:
            author = Author.objects.get(pk = str(authorId))
        except Author.DoesNotExist:
            return Response('Author does not exist', status= 404)
        
        if Author.objects.filter(authorId).exist(): #need varify the given author to follow exist in local db
            request = Follow_Request.objects.create(requestor = follower, requestee = authorId)
            InboxItem.objects.create(author = author , type = "F", contentId = request.pk)
            return Response(status=204)
        else:
            return Response("author to follow not found", status= 404)
    except KeyError:
        return Response('bad body format', status=400)
    

def handlePost(request, authorId):
    data = request.data
    
    try:
        id = data['id'].split('/posts/')[-1]
        try:
            author = Author.objects.get(pk = str(authorId))
        except Author.DoesNotExist:
            return Response('Author does not exist', status= 404)
        
        
        if not Post.objects.filter(pk = id).exists():
            id = data['id']
        
        InboxItem.objects.create(author = author, type = "P", contentId = id)
        return Response(status=204)
        
    except KeyError:
        return Response('bad body format', status=400)

functions = {"like": handleLike, "follow": handleFollows, "post": handlePost}


def putItemInInbox(request, authorId : str):
    try: 
        type = request.data["type"]
        return functions[type.lower()](request, authorId)
    except KeyError:
        return Response("'type' is not found", status=400) 




def clearInbox(request, authorId):

    InboxItem.objects.filter(author = authorId).delete()
    return Response(status=204)



@api_view(["POST", 'DELETE'])
@permission_classes([CustomPermissionFilter(allowedMethods=["POST"])])
def handleInbox(request, authorId : str):
    print(request.method)
    if request.method == "POST":
        return putItemInInbox(request, authorId)
    elif request.method == "DELETE":
        return clearInbox(request, authorId)
