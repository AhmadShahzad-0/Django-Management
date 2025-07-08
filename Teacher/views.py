from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Teacher
from django.contrib import messages

def add_teacher(request):
    if request.method == 'POST':
        # User fields
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('add_teacher')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('add_teacher')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Handle uploaded image
        image = request.FILES.get('teacher_image')

        # Create Teacher
        Teacher.objects.create(
            user=user,
            teacher_id=request.POST.get('teacher_id'),
            teacher_name=request.POST.get('teacher_name'),
            teacher_gender=request.POST.get('teacher_gender'),
            teacher_date_of_birth=request.POST.get('teacher_date_of_birth'),
            teacher_mobile=request.POST.get('teacher_mobile'),
            teacher_joining_date=request.POST.get('teacher_joining_date'),
            teacher_qualification=request.POST.get('teacher_qualification'),
            teacher_experience=request.POST.get('teacher_experience'),
            teacher_address=request.POST.get('teacher_address'),
            teacher_city=request.POST.get('teacher_city'),
            teacher_state=request.POST.get('teacher_state'),
            teacher_zip_code=request.POST.get('teacher_zipcode'),
            teacher_country=request.POST.get('teacher_country'),
            teacher_class=request.POST.get('teacher_class'),
            teacher_section=request.POST.get('teacher_section'),
            teacher_subject=request.POST.get('teacher_subject'),
            teacher_image=image
        )

        messages.success(request, "Teacher added successfully.")
        return redirect('teacher_list')  # Replace with your URL name

    return render(request, 'Teachers/add-teacher.html')

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'Teachers/teachers.html', {'teachers': teachers})

def edit_teacher(request):
    pass

def delete_teacher(request):
    pass