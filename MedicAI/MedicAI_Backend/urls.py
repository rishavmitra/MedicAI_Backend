from django.urls import path
from . import views

urlpatterns = [
    path('upload-report/',views.upload_report),
    path('chat-interact/',views.chat_interact),
    path('session-start/',views.session_start),
    path('fetch-sessions/',views.fetch_sessions),
    path('fetch-chats/',views.fetch_chats),
    path('delete-session/',views.delete_session),
    path('generate-summary/',views.generate_summary)
]