from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from django.contrib import messages
from School.utils import create_notification
from django.http import HttpResponseForbidden
from School.models import Notification
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.utils.dateparse import parse_date

User = get_user_model()

def add_teacher(request):
    if request.method == 'POST':
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

        dob = parse_date(request.POST.get('teacher_date_of_birth'))
        joining_date = parse_date(request.POST.get('teacher_joining_date'))
        if not dob or not joining_date:
            messages.error(request, "Invalid date format.")
            return redirect('add_teacher')

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                teacher = Teacher.objects.create(
                    user=user,
                    teacher_id=request.POST.get('teacher_id'),
                    teacher_name=request.POST.get('teacher_name'),
                    teacher_gender=request.POST.get('teacher_gender'),
                    teacher_date_of_birth=dob,
                    teacher_mobile=request.POST.get('teacher_mobile'),
                    teacher_joining_date=joining_date,
                    teacher_qualification=request.POST.get('teacher_qualification'),
                    teacher_experience=request.POST.get('teacher_experience'),
                    teacher_address=request.POST.get('teacher_address'),
                    teacher_city=request.POST.get('teacher_city'),
                    teacher_state=request.POST.get('teacher_state'),
                    teacher_zip_code=request.POST.get('teacher_zipcode'),
                    teacher_country=request.POST.get('teacher_country'),
                    teacher_image=request.FILES.get('teacher_image')
                )

                create_notification(request.user, f"Added Teacher: {user.username}")
                messages.success(request, "Teacher added successfully.")
                return redirect('teacher_list')

        except IntegrityError as e:
            messages.error(request, f"Database error: {e}")
            return redirect('add_teacher')

    return render(request, 'Teachers/add-teacher.html')

def teacher_list(request):
    teachers = Teacher.objects.all()
    unread_notification = request.user.notification_set.filter(is_read=False)
    context = {'teachers': teachers, 'unread_notification': unread_notification}
    return render(request, 'Teachers/teachers.html', context)

def view_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)
    return render(request, 'teachers/teacher-details.html', {'teacher': teacher})

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    user = teacher.user

    if request.method == 'POST':
        # Update User fields
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Check if username is changed and already taken
        if user.username != username and User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, "Username already exists.")
            return redirect('edit_teacher', pk=teacher.pk)

        user.username = username
        user.email = email
        user.save()


        # Handle optional password update
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password:
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('edit_teacher', pk=teacher.pk)
            user.set_password(password)
            user.save()

        # Handle uploaded image (optional)
        image = request.FILES.get('teacher_image')
        if image:
            teacher.teacher_image = image

        # Update Teacher model fields
        teacher.teacher_id = request.POST.get('teacher_id')
        teacher.teacher_name = request.POST.get('teacher_name')
        teacher.teacher_gender = request.POST.get('teacher_gender')
        teacher.teacher_date_of_birth = request.POST.get('teacher_date_of_birth')
        teacher.teacher_mobile = request.POST.get('teacher_mobile')
        teacher.teacher_joining_date = request.POST.get('teacher_joining_date')
        teacher.teacher_qualification = request.POST.get('teacher_qualification')
        teacher.teacher_experience = request.POST.get('teacher_experience')
        teacher.teacher_address = request.POST.get('teacher_address')
        teacher.teacher_city = request.POST.get('teacher_city')
        teacher.teacher_state = request.POST.get('teacher_state')
        teacher.teacher_zip_code = request.POST.get('teacher_zipcode')
        teacher.teacher_country = request.POST.get('teacher_country')
        teacher.save()
        create_notification(request.user, f"Updated Teacher: {teacher.teacher_name}")

        messages.success(request, "Teacher updated successfully.")
        return redirect('teacher_list')

    return render(request, 'Teachers/edit-teacher.html', {'teacher': teacher})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    create_notification(request.user, f"Deleted Teacher: {teacher.teacher_name}")
    messages.success(request, "Teacher deleted successfully.")
    return redirect('teacher_list')