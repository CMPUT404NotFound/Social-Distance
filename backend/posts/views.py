from typing import Union
from django.http.request import HttpRequest
from author.models import Author
from author.token import TokenAuth, NodeBasicAuth
from utils.request import makeRequest
from comment.documentation import NoSchemaTitleInspector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from drf_yasg.utils import swagger_auto_schema
from Followers.views import findFriends, findFollowers
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from inbox.models import InboxItem
from .models import Post, postsManager
from .serializers import PostsSerializer
from utils.request import parseIncomingRequest, ParsedRequest, returnGETRequest, ClassType
from django.http import HttpResponse

@swagger_auto_schema(method="get", tags=["Posts"])
@swagger_auto_schema(method="post", tags=["Posts"], field_inspectors=[NoSchemaTitleInspector], request_body=PostsSerializer)
@swagger_auto_schema(
    method="delete",
    tags=["Posts"],
)
@swagger_auto_schema(method="put", tags=["Posts"], field_inspectors=[NoSchemaTitleInspector], request_body=PostsSerializer)
@authentication_classes([TokenAuth(needAuthorCheck=["POST", "PUT", "DELETE"]), NodeBasicAuth])
@api_view(["GET", "POST", "DELETE", "PUT"])
@parseIncomingRequest(["GET"], ClassType.POST)
def managePost(request: Union[HttpRequest, ParsedRequest], author_id, post_id):
    '''
    
    http://localhost:8000/api/author/stuff/posts
    /project-api-404.herokuapp.com~api~author~20d63709-f5ce-43c7-87c1-c3c39ebd3910~posts~669b8267-0c5d-4d35-8f0d-f9d700ac0c1f~/
    '''
    if request.method != "GET": #front end wont need to call post, delete, put to other servers.
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response("no author under this id", status=status.HTTP_404_NOT_FOUND)

    
    # Getting the Post with post_id
    if request.method == "GET":
        #checking if it exists in our server
        if request.islocal:
            try:
                post = Post.objects.get(pk=request.id)
            except Post.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # getting friends list of that author  
            friend_id_string = findFriends(post.author_id) 
           
            # token auth will return a Author in this case(by pass entirely is not true), and nodebasicauth will return 'True' on success.
            usingTokenAuth = (
                    type(request.user) is Author
                )  

            # Checking if the user asking for the post is local or foreign
            is_friend = request.user.id in friend_id_string #regardless if friend or not, 

            # Seriliazing the data
            s = PostsSerializer(post, context={"request": request})
            
            # checking the visibility of the post
         
            is_it_visible = s.data.get("visibility") == "PUBLIC"
            
            # if visible then just return the post, no authentication 
            if is_it_visible:
                return Response(s.data, status=status.HTTP_200_OK)
            else: 
                if usingTokenAuth:
                    if request.user.id == post.author_id.id or is_friend:
                        return Response(s.data, status=status.HTTP_200_OK)
                    else:
                        return Response("no post under this id", status=status.HTTP_404_NOT_FOUND)
        
        #if post is not on our server then fetch from the other server
        else:
            return returnGETRequest(request.id)

    # PUT the specific post
    elif request.method == "PUT":
        
        
        data= dict(request.data)
        data["id"] = post_id
        data["author"] = author_id
        
        s = PostsSerializer(data=data)

        # checking if the post is valid
        if s.is_valid():
            s.data.author = author_id
            s.save()

            # getting friends list of that author  
            local_friend_id_string, foreign_author_id_string = findFriends(Author.objects.get(pk= author_id), True)
            follower_id_string = findFollowers(Author.objects.get(pk=author_id))

            # checking the visibility of the post
            if request.data.get("visibility") == "PUBLIC":
                is_it_visible = True
            else:
                is_it_visible = False

            # pushing it to the inbox according to the friend and follower 
            if(is_it_visible): #if visible then push to all the followers
                for follower in follower_id_string:
                    # checking if the follower is local or foreign
                    if(follower.startswith("http")):
                        return makeRequest("PUT", f"{follower if follower.endswith('/') else (follower + '/')  }inbox/", s.data)
                    else:
                        InboxItem.objects.create(author=Author.objects.get(pk = follower), type="P", contentId=post_id)
            
            else: # post is private
                for friend in foreign_author_id_string:
                    return makeRequest("PUT", f"{friend if friend.endswith('/') else (friend + '/')}inbox/", s.data)
                for local_freind in local_friend_id_string:    
                    InboxItem.objects.create(author=Author.objects.get(pk = local_freind), type="P", contentId=post_id)
            
            # Post created        
            return Response("Post created", s.data, status=status.HTTP_201_CREATED)
        
        # if data is not valid
        else:
            return Response("Data not valid, Post not created")  
     
    # Update a specific post 
    elif request.method == "POST":
        # check if the post exists
        try:
            post: Post = Post.objects.get(pk=post_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        s = PostsSerializer(instance=post, data=request.data)
        
       # check if the updated post is valid
        if s.is_valid():
            s.update()
            # getting friends list of that author  
            local_friend_id_string, foreign_author_id_string = findFriends(Author.objects.get(pk= author_id), True)
            follower_id_string = findFollowers(Author.objects.get(pk=author_id))

            # checking the visibility of the post
            if request.data.get("visibility") == "PUBLIC":
                is_it_visible = True
            else:
                is_it_visible = False

            # pushing it to the inbox according to the friend and follower 
            if(is_it_visible): #if visible then push to all the followers
                for follower in follower_id_string:
                    # checking if the follower is local or foreign
                    if(follower.startswith("http")):
                        return makeRequest("PUT", f"{follower if follower.endswith('/') else (follower + '/')  }inbox/", s.data)
                    else:
                        InboxItem.objects.create(author=Author.objects.get(pk = follower), type="P", contentId=post_id)
            
            else: # post is private
                for friend in foreign_author_id_string:
                    return makeRequest("PUT", f"{friend if friend.endswith('/') else (friend + '/')}inbox/", s.data)
                for local_freind in local_friend_id_string:    
                    InboxItem.objects.create(author=Author.objects.get(pk = local_freind), type="P", contentId=post_id)
            
            return Response("Post updated", status=status.HTTP_200_OK)
        
        # if post is not valid
        else:
            return Response("Post not updated, not a valid post", status=status.HTTP_400_BAD_REQUEST)

    # DELETE the post 
    elif request.method == "DELETE":
        try:
            post = Post.objects.filter(pk=post_id)
        except:
            return Response("Post doesnt exist",status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response("Post deleted", status=status.HTTP_204_NO_CONTENT)


# Create your views here.
@swagger_auto_schema(
    method="get",
    tags=["Posts"],
    operation_summary="Get posts of an author",
    operation_description="Get posts of author, with page & size pagination option. Request with no pagination to get all",
    field_inspectors=[NoSchemaTitleInspector],
    responses={200: PostsSerializer(many=True), 400: "Bad pagination format", 404: "Author or post not found"},
)
@swagger_auto_schema(
    method="post",
    tags=["Posts"],
    operation_summary="Create a post",
    field_inspectors=[NoSchemaTitleInspector],
    responses={204: "Post Created Successfully.", 400: "Bad post creation json format.", 404: "Author not found."},
    request_body=PostsSerializer,
)
@api_view(["GET", "POST"])
@authentication_classes([TokenAuth(needAuthorCheck=["POST"]), NodeBasicAuth])
@parseIncomingRequest(["GET"], ClassType.AUTHOR)
def getAllPosts(request: Union[HttpRequest, ParsedRequest], author_id):
   # checking if the author exists
    
    if request.method != "GET":
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response("no author under this id", status=status.HTTP_404_NOT_FOUND)    
    
    # Get all the post of that author   
    if request.method == "GET":
        # check if the post is in our server
        if request.islocal:
            try:
                # getting friends list of that author  
                friend_id_string = findFriends(Author.objects.get(pk= request.id))
                # print(Author.objects.get(pk = author_id))
                # print(friend_id_string)
                
                # token auth will return a Author in this case(by pass entirely is not true), and nodebasicauth will return 'True' on success.
                usingTokenAuth = (
                    type(request.user) is Author
                )  
                # checking if user is a friend and is in the server
                is_friend = request.user.id in friend_id_string #regardless if friend or not, 
                print(is_friend)
                params: dict = request.query_params
                
                # if user is from our server then check; foreign server wont ask for private post
                if usingTokenAuth:
                    if request.user.id == author_id or is_friend:
                        post = Post.objects.filter(author_id=request.id)
                    else:
                        post = Post.objects.filter(author_id=request.id).filter(visibility="PUBLIC").exclude(unlisted=True)
                else:
                    post = Post.objects.filter(author_id=request.id).filter(visibility="PUBLIC").exclude(unlisted=True)

                #doing pagination
                if "page" in params and "size" in params:  # make sure param has both page and size in order to paginate
                    try:
                        paginator = Paginator(post, int(params["size"]), allow_empty_first_page=True)  # create paginator with size
                        s = PostsSerializer(paginator.page(int(params["page"])), many=True)  # get requested page and serialize
                    except (ValueError, EmptyPage, PageNotAnInteger) as e:
                        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
                else:
                    s = PostsSerializer(post, context={"request": request}, many=True)
                
                # return post
                return Response(s.data, status=status.HTTP_200_OK)
            
            except Post.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        # if post is not on our server then go fetch it from pther server
        else:
            return returnGETRequest(request.id)
    
    #POST method
    elif request.method == "POST":
        # checking if the author exists
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response("no author under this id", status=status.HTTP_404_NOT_FOUND)
        
        # creating the post
        try:
            new_post = Post.objects.create(
                author_id=author,
                title=request.data.get("title", ""),
                visibility=request.data.get("visibility", "PUBLIC"),
                description=request.data.get("description", ""),
                content=request.data.get("content", ""),
                contentType=request.data.get("contentType", "plain"),
                source=request.data.get("source", ""),
                origin=request.data.get("origin", ""),
                unlisted=request.data.get("unlisted", "False"),
                categories=request.data.get("categories", ""),
                count=request.data.get("count", "0"),
            )
              
            new_post.save()
            # getting friends list of that author  
            local_friend_id_string, foreign_author_id_string = findFriends(Author.objects.get(pk= author_id), True)
            follower_id_string = findFollowers(Author.objects.get(pk=author_id))
            # checking the visibility of the post
            if request.data.get("visibility") == "PUBLIC":
                is_it_visible = True
            else:
                is_it_visible = False
                
            if(is_it_visible): #if visible then push to all the followers
                for follower in follower_id_string:
                    # checking if the follower is local or foreign
                    if(follower.startswith("http")):
                        return makeRequest("PUT", f"{follower if follower.endswith('/') else (follower + '/')  }inbox/", new_post.data)
                    else:
                        InboxItem.objects.create(author=Author.objects.get(pk = follower), type="P", contentId=new_post.pk)
                              
            else: # post is private
                for friend in foreign_author_id_string:
                    return makeRequest("PUT", f"{friend if friend.endswith('/') else (friend + '/')}inbox/", new_post.data)
                for local_freind in local_friend_id_string:    
                    InboxItem.objects.create(author=Author.objects.get(pk = local_freind), type="P", contentId= new_post.pk)
               
            return Response("Post is created",status=status.HTTP_204_NO_CONTENT)
            
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
