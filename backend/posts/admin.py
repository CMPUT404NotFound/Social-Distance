from django.contrib import admin
from django.contrib.admin import ModelAdmin
# Register your models here.
import django.forms as forms
from django.forms.models import ModelForm
from .models import Post

class PostAdmin(ModelAdmin):
    fields = ["title", "visibility","content"]
    list_display = ["title", "visibility","content"]

admin.site.register(Post, PostAdmin)