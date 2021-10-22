import re
from django.shortcuts import render


from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Author
from .serializers import *

# Create your views here.


@api_view(["GET", "POST"])
def author(request: Request, id):

    if request.method == "GET":

        try:
            author = Author.objects.get(pk=id)
            s = AuthorSerializer(author)
            return Response(s.data)

        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        # TODO implement some sort of security features? Any client can GET author info, but only authorized clients can create and update profile
        try:
            a: Author = Author.objects.get(pk=id)
            """Author exists already, should just update params (only displayName, github link, and prof img may be changed)"""
            post = request.data
            print(id, post, post.get("displayName", a.displayName))
            a.displayName = post.get("displayName", a.displayName)
            a.github = post.get("github", a.github)
            a.profileImage = post.get("profileImage", a.profileImage)
            a.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Author.DoesNotExist:
            pass
        #     """Author does not exists, check if params are valid then make an author entry."""
        #     # fixme id given in the request should be ignored. Make a id generator class
        #     s = AuthorSerializer(data=request.data)
        #     if s.is_valid():
        #         s.save()
        #         return Response(status=status.HTTP_201_CREATED)

        return Response("author not found!", status=status.HTTP_400_BAD_REQUEST)
