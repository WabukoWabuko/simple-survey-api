from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .models import Question, Response, Certificate
from .serializers import QuestionSerializer, ResponseSerializer
import os

class SurveyViewSet(viewsets.ViewSet):
    # GET /api/questions/
    @action(detail=False, methods=['GET'])
    def questions(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    # PUT /api/questions/responses/
    @action(detail=False, methods=['PUT'])
    def submit_response(self, request):
        serializer = ResponseSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            if request.FILES:
                for file in request.FILES.getlist('certificates'):
                    cert = Certificate(response=response, file_path=file.name)
                    cert.save()
                    with open(f'media/{file.name}', 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET /api/questions/responses/
    @action(detail=False, methods=['GET'])
    def responses(self, request):
        page = int(request.GET.get('page', 1))
        page_size = 10
        email_filter = request.GET.get('email_address', None)

        responses = Response.objects.all()
        if email_filter:
            responses = responses.filter(email_address=email_filter)

        total_count = responses.count()
        start = (page - 1) * page_size
        end = start + page_size
        paginated_responses = responses[start:end]

        serializer = ResponseSerializer(paginated_responses, many=True)
        response_data = {
            'current_page': page,
            'last_page': (total_count + page_size - 1) // page_size,
            'page_size': page_size,
            'total_count': total_count,
            'question_responses': serializer.data
        }
        return Response(response_data)

    # GET /api/questions/responses/certificates/<id>/
    @action(detail=True, methods=['GET'], url_path='responses/certificates')
    def download_certificate(self, request, pk=None):
        try:
            cert = Certificate.objects.get(id=pk)
            file_path = f'media/{cert.file_path}'
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=cert.file_path)
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)
