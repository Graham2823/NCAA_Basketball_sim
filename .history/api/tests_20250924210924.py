from django.test import TestCase

# Create your tests here.

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})

