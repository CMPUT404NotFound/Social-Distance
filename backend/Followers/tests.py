from django.http import response
from django.test import TestCase
from django.contrib.auth.models import User
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
        #self.create_author("test_user2", "test_password2")
        #self.create_author("test_user3", "test_password3")

    def create_author(self, username, display_name, github, profile_image, password):
        author = Author.objects.create_superuser(userName=username, displayName=display_name, github=github,
                                                 profileImage=profile_image, password=password)
        author.save()
        return author

    def test_get_authors(self):
        #Follower.objects.create(sender=self.usr1, receiver=self.usr2)
        response = self.client.get("/api/authors")
        assert response.status_code == 200

    # not working; something is up with the id
    # def test_get_followers(self):
    #     Follower.objects.create(sender=self.usr1, receiver=self.usr2)
    #     response = self.client.get("/api/author/{self.usr2.id}/followers")
    #     assert response.status_code == 200

    # def test_get_followers_individual(self):
    #     Follower.objects.create(sender=self.usr1, receiver=self.usr2)
    #     response = self.client.get(
    #         "/api/author/{self.usr2.id}/followers/{self.usr1.id}")
    #     assert response.status_code == 200
