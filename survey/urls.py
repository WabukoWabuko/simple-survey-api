from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('responses/', views.ResponseCreateView.as_view(), name='response_create'),  # PUT
    path('responses/', views.ResponseListView.as_view(), name='response_list'),     # GET
    path('certificates/<int:pk>/', views.CertificateDownloadView.as_view(), name='certificate_download'),
]
