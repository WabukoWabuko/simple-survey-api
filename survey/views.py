from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from .models import Question, Response, Certificate
from .serializers import QuestionSerializer, ResponseSerializer
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

# GET /api/questions/
class QuestionListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in QuestionListView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# PUT and GET /api/questions/responses/
class ResponseView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get('page', 1))
            page_size = 10
            email_filter = request.GET.get('email_address', None)

            queryset = Response.objects.all()
            if email_filter:
                queryset = queryset.filter(email_address=email_filter)

            total_count = queryset.count()
            start = (page - 1) * page_size
            end = min(start + page_size, total_count)  # Prevent out-of-range
            paginated_queryset = queryset[start:end]

            serializer = ResponseSerializer(paginated_queryset, many=True)
            response_data = {
                'current_page': page,
                'last_page': (total_count + page_size - 1) // page_size,
                'page_size': page_size,
                'total_count': total_count,
                'question_responses': serializer.data
            }
            return Response(response_data)
        except Exception as e:
            logger.error(f"Error in ResponseView GET: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            serializer = ResponseSerializer(data=request.data)
            if serializer.is_valid():
                response = serializer.save()
                if request.FILES:
                    for file in request.FILES.getlist('certificates'):
                        cert = Certificate(response=response, file_path=file.name)
                        cert.save()
                        file_path = f'media/{file.name}'
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure media dir exists
                        with open(file_path, 'wb+') as destination:
                            for chunk in file.chunks():
                                destination.write(chunk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in ResponseView PUT: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GET /api/questions/responses/certificates/<id>/
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
        except Exception as e:
            logger.error(f"Error in CertificateDownloadView: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
