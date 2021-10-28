from django.db import models

# Create your models here.
from author.models import Author
import uuid

Content_choices = {("P", "text/plain"), ("M", "text/markdown")}

# todo use real post instead
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return "place holder post"


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="post_comment"
    )

    author = models.ForeignKey(
        Author, related_name="+", on_delete=models.DO_NOTHING
    )  # related_name='+' means the reverse relation is not made

    comment = models.TextField(
        "comment", max_length=360, blank=True, null=False, default=""
    )

    content_type = models.CharField(
        "content-type",
        choices=Content_choices,
        max_length=1,
        default="P",
        null=False,
        blank=False,
    )

    published = models.DateTimeField("published", auto_now_add=True)

    def __str__(self):
        return f"{self.author}/{self.id}"
