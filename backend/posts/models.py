from django.db import models
import uuid
from backend import author
# Create your models here.
class posts(models.Model):
    visibility_choice = (("PUBLIC", "PRIVATE"))
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(author)
    title = models.CharField("title", max_length= 100, unique= False, null = False, blank  = False)
    visibility = models.CharField(choices=visibility_choice, blank = False, default = "PUBLIC")
    