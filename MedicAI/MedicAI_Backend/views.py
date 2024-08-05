from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .db_service import db_helper

# Create your views here.

@api_view(['POST'])
def upload_report(request):
    File = request.FILES['File']
    
    response = db_helper.upload_document(File)


    return Response(response)