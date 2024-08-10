from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .db_service import db_helper
from .ml_service import chat_service

# Create your views here.

@api_view(['POST'])
def upload_report(request):
    File = request.FILES['File']
    UserId = request.data['UserId']
    
    response = db_helper.upload_document(UserId, File)


    return Response(response)

@api_view(['POST'])
def chat_interact(request):
    user_message = request.data['Message']
    UserId = request.data['UserId']
    TimeStamp = request.data['TimeStamp']

    #______Code for openai_______#
    SystemMessage = chat_service.Call_OpenAI(user_message)

    response = db_helper.upload_chat(UserId,user_message,SystemMessage,TimeStamp)
    response.update({"SystemMessage":SystemMessage})

    return Response(response)

