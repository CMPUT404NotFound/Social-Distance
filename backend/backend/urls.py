"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.urls.conf import re_path
import author.views as authorViews
import posts.views as postsViews
import Followers.views as followerViews
import comment.views as commentViews
import inbox.views as inboxViews
import likes.views as likeviews
import nodes.views as nodeViews
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from author.token import TokenAuth

schema_view = get_schema_view(
    openapi.Info(
        title="Project Team 23 API",
        default_version="!!!",
        description='''
        ## Basic usage:  
        regsiter a new acc in /signup (admin:admin always works tho)  
        login via /login to receive the auth token, then apply token to swagger by clicking "Authorize" and type in "token <token_received>".  
        ---------------
        All api described in the specs looks and functions as expected, the few newly added api are for our frontend use only, and other
        nodes' access to them will be blocked by authentication.
        ---------------
        ## For Frontend: 
        A few api are modified to allow foreign or local link to be encoded in the request url, by remove `http://` and replace `/` with `~`.  
        For exmaple: `http://project-site.com/api/author/uuid-to-author/posts/uuid/` becomes
        `project-site.com~api~author~uuid-to-author~posts~uuid~`  
        And a GET request to the above post might look like `GET https://project-api-404.herokuapp.com/api/author/junkid/posts/project-site.com~api~author~uuid-to-author~posts~uuid~/`
        
        With <link> being the above encoded url, the following api are added/changed:
        + note: <link> can be an encoded link to either foreign site or our site, or just normal uuid, so that other server can access with no issues.
        + GET api/author/<link-author>/ (get any author by id)
        + follower stuff @phou
        + GET api/author/<link-author>/liked/ (all liked items for any author)
        + POST api/author/local-uuid/likes/comments/<link-comment>/ (local author likes link-comment)
        + POST api/author/local-uuid/likes/posts/<link-post>/ (local author likes link-post)
        + GET api/author/<ignored>/posts/<ignored>/comments/<link-comment>/likes/ (get likes of local or foreign )
        + GET api/author/<ignored>/posts/<link-post>/likes/
        + GET api/author/<ignored>/posts/<link-post>/comments/ (get comments of a post)
        + GET api/author/<link-author>/posts/ (all posts of a author)
        + GET api/author/<ignored>/posts/<link-post>/ (get since post by id)
        + GET api/nodes/ (get a list of nodes)
        + GET api/nodes/authors/ (get a list of all authors from every server, WIP)
        ''',
      
        #license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(TokenAuth(bypassEntirely=["GET"]),),
    permission_classes=(permissions.AllowAny,),
)
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url = 'https://project-api-404.herokuapp.com/api/', permanent = False)),
    path('admin/clearcache/', include('clearcache.urls')),
    re_path(r"^admin/?", admin.site.urls),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-~.]+)/?$", authorViews.handleAuthorById),
    
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-~.]+)/posts/?$", postsViews.getAllPosts),
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-]+)/posts/(?P<post_id>[A-Za-z0-9-~.]+)/?$", postsViews.managePost),
    re_path(r"^api/authors/?$", authorViews.getAllAuthors),
    re_path(r"^api/login/?$", authorViews.login),
    re_path(r"^api/signup/?$", authorViews.signUp),
    re_path(r"api/logout/?$", authorViews.logout),
    
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/posts/(?P<postId>[A-Za-z0-9-~.]+)/comments/?$", commentViews.handleComments),
    
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/friends/?$", followerViews.friendsView),
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-~.]+)/followers/?$", followerViews.getAllFollowers),
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-~.]+)/followers/(?P<follower_id>[A-Za-z0-9-~.]+)/?$", followerViews.addFollower),
    
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-~.]+)/inbox/?$", inboxViews.handleInbox),
    re_path(r'^api/author/(?P<authorId>[A-Za-z0-9-~.]+)/liked/?$', likeviews.getLiked ),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/posts/(?P<postId>[A-Za-z0-9-~.]+)/likes/?$", likeviews.getPostLikes),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/posts/(?P<postId>[A-Za-z0-9-~.]+)/comments/(?P<commentId>[A-Za-z0-9-~.]+)/likes/?$", likeviews.getCommentLikes),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/likes/posts/(?P<postId>[A-Za-z0-9-~.]+)/?$", likeviews.addLikePost),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/likes/comments/(?P<commentId>[A-Za-z0-9-~.]+)/?$", likeviews.addLikeComment),
    
    re_path(r"^api/nodes/?$", nodeViews.getNodes),

    #api paths
    re_path(
        r"^api/?$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path(
    #     "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    # ),
]
