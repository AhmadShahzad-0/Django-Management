from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import uuid

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    hod = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_teacher': True},  # Only teacher users can be HOD
        related_name='departments_led'
    )
    start_date = models.DateField(default=timezone.now)

    def num_students(self):
        return self.students.count()  # Reverse relation from Student model

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100, default='OOP')
    class_name = models.CharField(max_length=100, default='9')  # e.g., "BSc Computer Science", "Grade 10"

    def __str__(self):
        return f"{self.name} ({self.class_name})"
    
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
