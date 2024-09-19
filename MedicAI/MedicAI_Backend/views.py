from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .db_service import db_helper
from .ml_service import chat_service
from .ml_service.chat_service import document_information

# Create your views here.

document_info_class = None

@api_view(['POST'])
def upload_report(request):
    File = request.FILES['File']
    UserId = request.data['UserId']
    SessionId=request.data['SessionId']
    
    document_obj = document_information()

    response = db_helper.upload_document(UserId, File,SessionId,document_obj)
    
    global document_info_class
    document_info_class = document_obj

    return Response(response)

@api_view(['POST'])
def chat_interact(request):
    user_message = request.data['Message']
    UserId = request.data['UserId']
    TimeStamp = request.data['TimeStamp']
    SessionId=request.data['SessionId']
    SerialNum = request.data['SerialNum']

    #______Code for openai_______#
    SystemMessage = chat_service.Call_OpenAI(user_message,document_info_class)

    response = db_helper.upload_chat(UserId,user_message,SystemMessage,TimeStamp,SessionId,SerialNum)
    response.update({"SystemMessage":SystemMessage})

    return Response(response)


@api_view(['POST'])
def session_start(request):
    SessionId=request.data['SessionId']
    UserId = request.data['UserId']

    print(SessionId,UserId)

    response = db_helper.upload_sessions(SessionId,UserId)

    return Response(response)