from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import test_collection

# Create your views here.

@api_view(['POST'])
def upload_report(request):
    records = {
        "first_name":"Rishav"
    }
    test_collection.insert_one(records)
    return Response("Request Recieved")