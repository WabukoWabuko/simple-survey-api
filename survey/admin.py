from django.contrib import admin
from .models import Question, Option, Response, Certificate

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Response)
admin.site.register(Certificate)
