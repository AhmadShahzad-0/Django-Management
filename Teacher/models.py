from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    teacher_gender = models.CharField(max_length=15, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    teacher_date_of_birth = models.DateField()
    teacher_mobile = models.CharField(max_length=15)
    teacher_joining_date = models.DateField()
    teacher_qualification = models.CharField(max_length=50)
    teacher_experience = models.CharField(max_length=100)
    teacher_image = models.ImageField(upload_to='teachers/', blank=True, null=True)

    # Address
    teacher_address = models.TextField()
    teacher_city = models.CharField(max_length=100)
    teacher_state = models.CharField(max_length=100)
    teacher_zip_code = models.CharField(max_length=20)
    teacher_country = models.CharField(max_length=100)

    def __str__(self):
        return self.teacher_name
    