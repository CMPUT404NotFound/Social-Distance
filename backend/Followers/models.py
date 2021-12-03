from typing import List, Union
from django.db import models
import uuid

from django.db.models.query import QuerySet
from author.models import *
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # sender = models.ForeignKey(
    #     Author, on_delete=models.CASCADE, related_name="sender")
    # sender = JSONField()
    sender = models.CharField(max_length=100)
    receiver = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="receiver")


class Follow_Request(models.Model):
    # requestor = models.ForeignKey(
    #     Author, on_delete=models.CASCADE, related_name="requestor")
    requestor = models.CharField(max_length=100)
    # requestor = JSONField()
    requestee = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="requestee")


class Following(models.Model):
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    following = models.CharField(max_length=200)
    #following = models.JSONField()
    
    
def findFriends(authorId: Union[str, Author]) -> List[str]:
    
    '''
    returns of list of ids of users(local or foreign) who are friends with the author provided.
    '''
    
    followers : QuerySet = Follower.objects.filter(receiver = authorId).values("sender")
    followings : QuerySet = Following.objects.filter(author = authorId).values("following")
    
    
    friends =  followers.intersection(followings) 
    
    return [str(friend['sender']) for friend in friends]