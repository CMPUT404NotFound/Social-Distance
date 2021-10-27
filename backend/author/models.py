from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class AuthorManager(BaseUserManager):
    def create_user(self, displayName, github="", profileImage="", password=None):

        if not displayName:
            raise ValueError("Users must have a displayName")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            displayName=displayName,
            github=github,
            profileImage=profileImage,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, displayName, github="", profileImage="", password=None):

        user = self.create_user(displayName, github, profileImage, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class Author(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    displayName = models.CharField(
        "displayName",
        max_length=40,
        unique=True,
        null=False,
        blank=False,
    )  # max 40 chars should be more than enough
    github = models.URLField(
        "github", max_length=60, blank=True
    )  # len('https://github.com/'), and max user name length on github is 39 chars
    profileImage = models.URLField("profileImage", blank=True)

    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"author: {self.displayName}, id: {self.id}"

    objects : AuthorManager = AuthorManager()

    USERNAME_FIELD = "displayName"
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
