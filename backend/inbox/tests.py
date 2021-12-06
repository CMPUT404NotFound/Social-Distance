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

class InboxTestCase(TestCase):
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

    def get_author_inbox(self):
        str_id1 = str(self.usr1.id)
        response = self.client.get(f"/api/author/{str_id1}/inbox")
        assert 100 < response.status_code < 300

    def send_follow_to_inbox(self):
        str_id1 = str(self.usr1.id)
        str_id2 = str(self.usr1.id)
        post_id = str(self.post.id)
        data = {
    "type": "Follow",      
    "summary":"",
    "actor":{
                    "type":"author",
                    "id":self.usr1.id,
                    "url":self.usr1.id,
                    "host":"project-api-404.herokuapp.com/",
                    "displayName":self.usr1.displayName,
                    "github": self.usr1.github,
                    "profileImage": self.usr1.profileImage,
                },
                "object":{
                    "type":"author",
                    # ID of the Author
                    "id":self.usr2.id,
                    # the home host of the author
                    "host":"project-api-404.herokuapp.com/",
                    # the display name of the author
                    "displayName":self.usr2.displayName,
                    # url to the authors profile
                    "url":self.usr2.id,
                    # HATEOS url for Github API
                    "github": self.usr2.github,
                    # Image from a public domain
                    "profileImage": self.usr2.profileImage,
                }
            }
        response = self.client.post(f"/api/author/{str_id2}/inbox", data)
        assert 100 < response.status_code < 300
                            
