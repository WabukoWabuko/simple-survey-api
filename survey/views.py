from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from .models import Question, Response, Certificate
from .serializers import QuestionSerializer, ResponseSerializer
import os

# GET /api/questions
@api_view(['GET'])
def get_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

# PUT /api/questions/responses
@api_view(['PUT'])
def submit_response(request):
    serializer = ResponseSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.save()
        # Handle file uploads
        if request.FILES:
            for file in request.FILES.getlist('certificates'):
                cert = Certificate(response=response, file_path=file.name)
                cert.save()
                # Save file to disk (simple for now)
                with open(f'media/{file.name}', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /api/questions/responses
@api_view(['GET'])
def get_responses(request):
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

# GET /api/questions/responses/certificates/{id}
@api_view(['GET'])
def download_certificate(request, id):
    try:
        cert = Certificate.objects.get(id=id)
        file_path = f'media/{cert.file_path}'
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=cert.file_path)
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    except Certificate.DoesNotExist:
        return Response({'error': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)
