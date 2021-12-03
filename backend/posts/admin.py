from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
import django.forms as forms
from django.forms.models import ModelForm
from .models import Post


class PostAdmin(ModelAdmin):
    fields = ["author_id", "title", "visibility", "content","description","contentType","unlisted"]
    list_display = ["post_id", "title", "visibility","content","description","contentType","unlisted"]


admin.site.register(Post, PostAdmin)
