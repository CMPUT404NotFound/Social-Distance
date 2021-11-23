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
import author.views as authorViews
import posts.views as postsViews
import Followers.views as followerViews
import comment.views as commentViews
import inbox.views as inboxViews
import likes.views as likeviews
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from posts.models import Post

...

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
    permission_classes=(permissions.AllowAny,),
)
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url = 'https://cmput404project.netlify.app/', permanent = False)),
    path("admin/", admin.site.urls),
    path("api/author/<slug:id>", authorViews.handleAuthorById),
    path("api/author/<uuid:author_id>/posts", postsViews.getAllPosts),
    path("api/authors", authorViews.getAllAuthors),
    path("api/login", authorViews.login),
    path("api/signup", authorViews.signUp),
    path("api/author/<slug:authorId>/post/<slug:postId>/comments", commentViews.handleComments),
    
    path("api/author/<uuid:id>/followers", followerViews.getAllFollowers),
    path("api/author/<uuid:author_id>/followers/<uuid:follower_id>", followerViews.addFollower),
    
    path("api/author/<uuid:authorId>/inbox", inboxViews.handleInbox),
    path('api/author/<uuid:authorId>/liked', likeviews.getLiked ),
    path("api/author/<uuid:authorId>/posts/<uuid:postId>/likes", likeviews.getPostLikes),
    path("api/author/<uuid:authorId>/posts/<uuid:postId>/comments/<uuid:commentId>/likes", likeviews.getCommentLikes),

    #api paths
    path(
        "api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
