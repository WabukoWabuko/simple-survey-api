from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.get_questions, name='get_questions'),
    path('questions/responses/', views.submit_response, name='submit_response'),
    path('questions/responses/', views.get_responses, name='get_responses'),
    path('questions/responses/certificates/<int:id>/', views.download_certificate, name='download_certificate'),
]
