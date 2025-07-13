from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# Create your models here.
class Department(models.Model):
    department_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    head_of_department = models.CharField(max_length=100)
    start_date = models.DateField()
    number_of_students = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.department_id})"
    
class Subject(models.Model):
    subject_id = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    subject_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_class})"
    
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
