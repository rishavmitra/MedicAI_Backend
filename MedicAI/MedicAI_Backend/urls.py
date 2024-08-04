from django.urls import path
from . import views

urlpatterns = [
    path('upload-report/',views.upload_report)
]