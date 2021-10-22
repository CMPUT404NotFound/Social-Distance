from django.shortcuts import render



from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Author
from .serializers import *

# Create your views here.


@api_view(['GET', 'POST'])
def author(request: Request, id):
    
    if request.method == 'GET':
        try:    
            author = Author.objects.get(id = id)
            s = AuthorSerializer(author)
            return Response(s.data)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)