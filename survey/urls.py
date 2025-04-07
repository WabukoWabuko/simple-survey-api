from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.get_questions, name='get_questions'),
    path('questions/responses/', views.handle_responses, name='handle_responses'),  # Handles both PUT and GET
    path('questions/responses/certificates/<int:id>/', views.download_certificate, name='download_certificate'),
]
