from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import views
from author.models import *
from Followers.models import *
from posts.models import *
from comment.models import *
from logging import exception
from django.http import response
from django.http import request
from django.http.request import HttpRequest

# Create your tests here.
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentTestCase(TestCase):
    def setUp(self):
        response = self.client.get("")
        self.request = response.wsgi_request
        self.usr1 = self.create_author("test_user1", "test_user1",
                                       "test_user1@github", "", "test_password1")
        self.usr2 = self.create_author("test_user2", "test_user2",
                                       "test_user2@github", "", "test_password2")
        self.usr3 = self.create_author("test_user3", "test_user3",
                                       "test_user3@github", "", "test_password3")
        self.post = self.create_post(self.usr1, "test_title", "test_content")
        self.comment = self.create_comment(self.usr2, self.post, "test_content")

    def create_author(self, username, display_name, github, profile_image, password):
        author = Author.objects.create_superuser(userName=username, displayName=display_name, github=github,
                                                 profileImage=profile_image, password=password)
        author.save()
        return author

    def create_post(self, author, title, content):
        post = Post.objects.create(author=author, title=title, content=content)
        post.save()
        return post

    def create_comment(self, author, post, content):
        comment = Comment.objects.create(author=author, post=post, content=content)
        comment.save()
        return comment

    def get_comments_of_post(self, post):
        str_id1 = str(self.usr1.id)
        post_id = str(self.post.id)
        response = self.client.get(f"/api/author/{str_id1}/posts/{post_id}")
        assert 100 < response.status_code < 300

    def create_comment_through_request(self):
        str_id1 = str(self.usr1.id)
        post_id = str(self.post.id)
        data = {
                    "type":"comment",
                    "author":{
                        "type":"author",
                        # ID of the Author (UUID)
                        "id":str_id1,
                        # url to the authors information
                        "url":str_id1,
                        "host": "https://project-api-404.herokuapp.com/api",
                        "displayName":str(self.usr1.displayName),
                        # HATEOS url for Github API
                        "github": str(self.usr1.github),
                        # Image from a public domain
                        "profileImage": str(self.usr1.github)
                    },
                    "comment":"Sick Olde English",
                    "contentType":"text/markdown",
                    # ISO 8601 TIMESTAMP
                    "published":"2015-03-09T13:07:04+00:00",
                    # ID of the Comment (UUID)
                    "id": self.comment.id,
                }
        response = self.client.post(f"/api/author/{str_id1}/posts/{post_id}/comments", data)
        assert 100 < response.status_code < 300
                            
