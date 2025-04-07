from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/responses/', views.ResponseView.as_view(), name='response_view'),
    path('questions/responses/certificates/<int:pk>/', views.CertificateDownloadView.as_view(), name='certificate_download'),
]
