from django.db import models
import uuid
from author.models import Author

# Create your models here.

visibility_choice = {("PU", "PUBLIC"), ("PR", "PRIVATE")}


class postsManager(models.Model):
    pass

class posts(models.Model):

    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="post_author"
    )
    title = models.CharField(
        "title", max_length=100, unique=False, null=False, blank=False
    )
    visibility = models.CharField(
        choices=visibility_choice, max_length=8, null=False, blank=False, default="PU"
    )
    content = models.TextField("content", max_length=200, blank=True)

    def __str__(self):
        return "place holder post"
