from django.db import models

# Create your models here.

from author.models import Author

typeChoices = [("P", "Post"), ("F", "Follow"), ("L", "Like")]


class InboxItem(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    type = models.CharField(
        max_length=1, choices=typeChoices, default="P", null=False, blank=False
    )

    contentId = models.CharField(max_length=300, null=False, blank=False, default="")
