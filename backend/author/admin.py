from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
import django.forms as forms
from django.forms.models import ModelForm
from .models import Author
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin


class UserCreationForm(ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    is_admin = forms.BooleanField(label="Admin", required=False)

    class meta:
        model = Author
        fields = [
            "userName",
            "displayName",
            "github",
            "profileImage",
            "isLocalUser",
            "host",
        ]

    def clean_password2(self):
        # clean_<variable>() is called to clean the variable. Here te 2 passwords are compared to make sure they match.
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    # for updating values of existing users
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Author
        fields = [
            "displayName",
            "password",
            "is_admin",
            "github",
            "profileImage",
            "host",
        ]


class AuthorAdmin(UserAdmin):

    # define forms for creating new users and updating existing users

    form = UserChangeForm
    add_form = UserCreationForm

    # im not sure what the following does
    # help
    list_display = ("displayName", "github", "profileImage", "is_admin")
    list_filter = ("is_admin",)
    # fields for when modifying an existing user
    fieldsets = (
        (None, {"fields": ("userName", "password")}),
        ("Personal info", {"fields": ("displayName", "github", "profileImage")}),
        ("Permissions", {"fields": ("is_admin", "host")}),
    )

    # fields for when adding a new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "userName",
                    "password1",
                    "password2",
                    "is_admin",
                    "isLocalUser",
                    "displayName",
                    "github",
                    "profileImage",
                    "host",
                ),
            },
        ),
    )

    # for when displaying in a list
    search_fields = ("displayName",)
    ordering = ("displayName",)
    filter_horizontal = ()


admin.site.register(Author, AuthorAdmin)
admin.site.unregister(Group)
