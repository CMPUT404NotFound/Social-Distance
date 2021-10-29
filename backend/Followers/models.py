from django.db import models
import uuid
from author.models import *
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class Follower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="receiver")


class Follow_Request(models.Model):
    requestor = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="requestor")
    requestee = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="requestee")
