from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from .models import Question, Response, Certificate
from .serializers import QuestionSerializer, ResponseSerializer
import os

# GET /api/questions/
class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# PUT /api/responses/
class ResponseCreateView(generics.CreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def perform_create(self, serializer):
        response = serializer.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('certificates'):
                cert = Certificate(response=response, file_path=file.name)
                cert.save()
                with open(f'media/{file.name}', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

# GET /api/responses/
class ResponseListView(generics.ListAPIView):
    serializer_class = ResponseSerializer

    def get_queryset(self):
        email_filter = self.request.GET.get('email_address', None)
        queryset = Response.objects.all()
        if email_filter:
            queryset = queryset.filter(email_address=email_filter)
        return queryset

    def list(self, request, *args, **kwargs):
        page = int(request.GET.get('page', 1))
        page_size = 10
        queryset = self.get_queryset()
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]
        serializer = self.get_serializer(paginated_queryset, many=True)
        response_data = {
            'current_page': page,
            'last_page': (total_count + page_size - 1) // page_size,
            'page_size': page_size,
            'total_count': total_count,
            'question_responses': serializer.data
        }
        return Response(response_data)

# GET /api/certificates/<id>/
class CertificateDownloadView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            cert = Certificate.objects.get(id=pk)
            file_path = f'media/{cert.file_path}'
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=cert.file_path)
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)
