from django.db import models
import uuid

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from backend.settings import SITE_ADDRESS

class AuthorManager(BaseUserManager):
    def create_user(
        self,
        userName=None,
        displayName="",
        github="",
        profileImage="",
        password=None,
        is_active = False
    ):
        
        if not userName:
            raise ValueError("Users must have a userName")
        if not password:
            raise ValueError("Users must have a password")


        user = self.model(
            id=uuid.uuid4(),
            userName=userName,
            displayName=displayName if displayName else userName,
            github=github,
            profileImage=profileImage,
            is_active = is_active
        )
        user.set_password(password )
        user.save(using=self._db)
        return user

    def create_superuser(
        self, userName, displayName="", github="", profileImage="", password=None
    ):
        user = self.create_user(userName, displayName, github, profileImage, password, True)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Author(AbstractBaseUser):
    '''
    TODO let admin activate/deactivate authenticate.
    '''
    
    
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=200)

    displayName = models.CharField(max_length=40, null=False, blank=True, default="")

    userName = models.CharField(
        "userName",
        max_length=40,
        unique=True,
        null=False,
        blank=False,
        default="defaultName",
    )  # max 40 chars should be more than enough
    
    github = models.URLField(
        "github", max_length=60, blank=True, null=False
    )  # len('https://github.com/'), and max user name length on github is 39 chars
    
    profileImage = models.URLField("profileImage", blank=True, null=False)

    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"author: {self.displayName}, id: {self.id}"

    objects: AuthorManager = AuthorManager()

    USERNAME_FIELD = "userName"
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
