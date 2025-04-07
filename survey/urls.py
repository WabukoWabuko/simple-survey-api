from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the ViewSet
router = DefaultRouter()
router.register(r'', views.SurveyViewSet, basename='survey')

urlpatterns = [
    path('', include(router.urls)),  
]
