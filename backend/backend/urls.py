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
        title="Name Undecided API",
        default_version="v0",
        description="Documentation for api of this app",
        #terms_of_service="https://www.google.com/policies/terms/",
        #contact=openapi.Contact(email="contact@snippets.local"),
        #license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(TokenAuth(bypassEntirely=["GET"]),),
    permission_classes=(permissions.AllowAny,),
)
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url = 'https://project-api-404.herokuapp.com/api/', permanent = False)),
    re_path(r"^admin/?", admin.site.urls),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-~.]+)/?$", authorViews.handleAuthorById),
    
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-~.]+)/posts/?$", postsViews.getAllPosts),
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-]+)/posts/(?P<post_id>[A-Za-z0-9-~.]+)/?$", postsViews.managePost),
    re_path(r"^api/authors/?$", authorViews.getAllAuthors),
    re_path(r"^api/login/?$", authorViews.login),
    re_path(r"^api/signup/?$", authorViews.signUp),
    
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/post/(?P<postId>[A-Za-z0-9-~.]+)/comments/?$", commentViews.handleComments),
    
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/friends/?$", followerViews.friendsView),
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-~.]+)/followers/?$", followerViews.getAllFollowers),
    re_path(r"^api/author/(?P<author_id>[A-Za-z0-9-~.]+)/followers/(?P<follower_id>[A-Za-z0-9-~.]+)/?$", followerViews.addFollower),
    
    re_path(r"^api/author/<(?P<authorId>[A-Za-z0-9-~.]+)/inbox/?$", inboxViews.handleInbox),
    re_path(r'^api/author/(?P<authorId>[A-Za-z0-9-~.]+)/liked/?$', likeviews.getLiked ),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/posts/(?P<postId>[A-Za-z0-9-~.])/likes/?$", likeviews.getPostLikes),
    re_path(r"^api/author/(?P<authorId>[A-Za-z0-9-]+)/posts/(?P<postId>[A-Za-z0-9-~.])/comments/(?P<commentId>[A-Za-z0-9-~.])/likes/?$", likeviews.getCommentLikes),
    
    re_path(r"^api/nodes/?$", nodeViews.getNodes),

    #api paths
    re_path(
        r"^api/?",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path(
    #     "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    # ),
]
