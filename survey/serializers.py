from rest_framework import serializers
from .models import Question, Option, Response, Certificate

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'value', 'multiple']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'name', 'type', 'required', 'text', 'description', 'options']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'file_path']

class ResponseSerializer(serializers.ModelSerializer):
    certificates = CertificateSerializer(many=True, read_only=True)

    class Meta:
        model = Response
        fields = ['id', 'full_name', 'email_address', 'description', 'gender', 'programming_stack', 'date_responded', 'certificates']
