from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
import django.forms as forms
from django.forms.models import ModelForm
from .models import Comment, Post


# class CommentCreationForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["post", "author", "comment", "content-type"]

#     def save(self, commit=True):
#         comment = super(CommentCreationForm, self).save(commit=False)
#         if commit:
#             comment.save()
#         return comment


# class CommentChangeForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["comment", "content-type"]


class CommentAdmin(ModelAdmin):

    fields = [
        "post",
        "author",
        "comment",
        "contentType",
    ]
    list_display = ["post", "author", "comment", "contentType", "published"]


class PostAdmin(ModelAdmin):
    fields = ["id", "content"]
    list_display = ["id", "content"]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
