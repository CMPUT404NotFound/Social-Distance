from django.db import models

# Create your models here.

import uuid

Content_choices = (("P", "text/plain"), ("M", "text/markdown"))

from posts.models import Post


class Comment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )

    author = models.CharField(
        "id to local or foreign author", max_length=100, blank=True, null=False
    )

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
