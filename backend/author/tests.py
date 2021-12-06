from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import views
from author.models import *
from Followers.models import *
from logging import exception
from django.http import response
from django.http import request
from django.http.request import HttpRequest

# Create your tests here.
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorTestCase(TestCase):
    def setUp(self):
        response = self.client.get("")
        self.request = response.wsgi_request
        self.usr1 = self.create_author("test_user1", "test_user1",
                                       "test_user1@github", "", "test_password1")
        self.usr2 = self.create_author("test_user2", "test_user2",
                                       "test_user2@github", "", "test_password2")
        self.usr3 = self.create_author("test_user3", "test_user3",
                                       "test_user3@github", "", "test_password3")

    def create_author(self, username, display_name, github, profile_image, password):
        author = Author.objects.create_superuser(userName=username, displayName=display_name, github=github,
                                                 profileImage=profile_image, password=password)
        author.save()
        return author

    def test_get_authors(self):
        #200 when disable tokens
        # Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        response = self.client.get("/api/authors")
        assert 100 < response.status_code < 300

    def test_get_author_by_id(self):
        #200 when disable tokens
        str_id1 = str(self.usr2.id)
        response = self.client.get(f"/api/author/{str_id1}/")
        assert 100 < response.status_code < 300
    

            

