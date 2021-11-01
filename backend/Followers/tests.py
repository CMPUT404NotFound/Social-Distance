from logging import exception
from django.http import response
from django.http import request
from django.http.request import HttpRequest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import views
from author.models import *
from Followers.models import *

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your tests here.


class FollowerTestCase(TestCase):
    def setUp(self):
        response = self.client.get("")
        self.request = response.wsgi_request.user
        self.usr1 = self.create_author("test_user1", "test_user1",
                                       "test_user1@github", "", "test_password1")
        self.usr2 = self.create_author("test_user2", "test_user2",
                                       "test_user2@github", "", "test_password2")
        self.usr3 = self.create_author("test_user3", "test_user3",
                                       "test_user3@github", "", "test_password3")
        # self.create_author("test_user2", "test_password2")
        # self.create_author("test_user3", "test_password3")

    def create_author(self, username, display_name, github, profile_image, password):
        author = Author.objects.create_superuser(userName=username, displayName=display_name, github=github,
                                                 profileImage=profile_image, password=password)
        author.save()
        return author

    def test_get_authors(self):
        # Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        response = self.client.get("/api/authors")
        assert response.status_code == 200

    # not working; something is up with the id
    def test_get_followers_by_id(self):
        Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        str_id2 = str(self.usr2.id)
        response = self.client.get(f"/api/author/{str_id2}/followers")
        # print("RESPONSE: ", response.json()[0]['id'])
        assert response.status_code == 200

    def test_get_single_follower_by_id(self):
        Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        str_id1 = str(self.usr1.id)
        str_id2 = str(self.usr2.id)
        response = self.client.get(
            f"/api/author/{str_id2}/followers/{str_id1}")
        assert response.status_code == 200

    def test_delete_follower_of_id(self):
        Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        str_id1 = str(self.usr1.id)
        str_id2 = str(self.usr2.id)
        response = self.client.delete(
            f"/api/author/{str_id2}/followers/{str_id1}")
        assert response.status_code == 200

    def test_follower_duplication(self):
        Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        str_id1 = str(self.usr1.id)
        str_id2 = str(self.usr2.id)
        response = self.client.put(
            f"/api/author/{str_id2}/followers/{str_id1}")
        response2 = self.client.put(
            f"/api/author/{str_id2}/followers/{str_id1}")
        assert response2.status_code == 400

    def test_follower_not_exist(self):
        Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        str_id1 = str(self.usr1.id)
        str_id3 = str(self.usr3.id)
        response = self.client.get(
            f"/api/author/{str_id3}/followers/{str_id1}")
        assert response.status_code == 404
