from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .db_service import db_helper
from .ml_service import chat_service
from .ml_service.chat_service import document_information
from datetime import datetime

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

    if user_message.startswith('File') and 'has been uploaded' in user_message:
        # Fixed system message for file uploads
        SystemMessage = "Thank you for the reference document."
    else:
        # If not a file upload message, call OpenAI to generate a dynamic system message
        SystemMessage = chat_service.Call_OpenAI(user_message, document_info_class)

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



@api_view(['POST'])
def fetch_sessions(request):
    UserId = request.data  # Safely extract UserId from request
    if UserId == '':
        print("error")
        return Response({"error": "UserId not provided"}, status=400)  # Handle missing UserId

    try:
        print(f"Fetching sessions for UserID: {UserId}")
        
        sessions = db_helper.get_sessions(UserId.get('UserId'))
        
        # Extract SessionIds only from the sessions
        session_ids = [session['SessionId'] for session in sessions]
        
        
        return Response({"sessions": sessions}, status=200)
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug the error
        return Response({"error": str(e)}, status=500)  # Return the error message
    

@api_view(['POST'])
def fetch_chats(request):
    session_id = request.data.get('sessionId')
    chats, files =db_helper.get_chats(session_id)

    document_obj = document_information()

    if len(files)>0:
        file_id = files[-1]
        db_helper.download_document(file_id=file_id,document_obj=document_obj)

        global document_info_class
        document_info_class = document_obj
    
    # print(chats)
    response_data = []
    for chat in chats:
        try:
            chat['timestamp'] = datetime.fromisoformat(chat['timestamp']).isoformat()
        except ValueError:
            pass
        response_data.append({
            'id': str(chat['_id']),  
            'UserMessage': chat['UserMessage'],
            'SystemMessage': chat['SystemMessage'],
            'timestamp': chat['timestamp'],
            'SerialNum' : chat['SerialNum']
        })
    

    return Response({'chats': response_data})


@api_view(['DELETE'])
def delete_session(request):
    # Extract UserId and sessionId from request data
    user_id = request.data.get('UserId')
    session_id = request.data.get('sessionId')  # Use sessionId from request body
    print('Here',session_id)

    if not user_id or not session_id:
        print("Error: UserId or sessionId not provided")
        return Response({"error": "UserId and sessionId must be provided"}, status=400)

    try:
        print(f"Attempting to delete session {session_id} for UserID: {user_id}")

        # Call the helper function to delete the session and related data
        deleted = db_helper.delete_session(user_id, session_id)

        if deleted:
            return Response({"message": "Session and related data deleted successfully."}, status=204)
        else:
            return Response({"error": "Session not found or could not be deleted."}, status=404)

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug the error
        return Response({"error": str(e)}, status=500)
