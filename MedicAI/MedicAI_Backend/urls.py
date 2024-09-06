from django.urls import path
from . import views

urlpatterns = [
    path('upload-report/',views.upload_report),
    path('chat-interact/',views.chat_interact),
    path('session-start/',views.session_start)
]