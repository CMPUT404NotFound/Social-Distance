from django.db import models

# Create your models here.
from author.models import Author
import uuid

Content_choices = {("P", "text/plain"), ("M", "text/markdown")}

from posts.models import posts

class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(
        posts, on_delete=models.CASCADE, related_name="post_comments"
    )

    author = models.ForeignKey(
        Author, related_name="+", on_delete=models.DO_NOTHING
    )  # related_name='+' means the reverse relation is not made

    comment = models.TextField(
        "comment", max_length=360, blank=True, null=False, default=""
    )

    contentType = models.CharField(
        "contentType",
        choices=Content_choices,
        max_length=1,
        default="P",
        null=False,
        blank=False,
    )

    published = models.DateTimeField("published", auto_now_add=True)

    def __str__(self):
        return f"{self.author}/{self.id}"
