from django.db import models

class Question(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20)  # short_text, email, long_text, choice, file
    required = models.CharField(max_length=3)  # yes, no
    text = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    multiple = models.CharField(max_length=3)  # yes, no

    def __str__(self):
        return self.value

class Response(models.Model):
    full_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    description = models.TextField()
    gender = models.CharField(max_length=20)
    programming_stack = models.TextField()  # Comma-separated values
    date_responded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email_address}"

class Certificate(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=200)  # Path to file

    def __str__(self):
        return f"Cert for {self.response.full_name}"
