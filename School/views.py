from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Subject, Notification
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def index(request):
    return render(request, "authentication/login.html", {})

def dashboard(request):
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notification.count()
    return render(request, "Students/student-dashboard.html", {
        'unread_notification_count': unread_notification_count,})

def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden

def teacher_dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to access this page.")
    
    # Assuming you have a field like `is_teacher` on your user model or profile
    if not hasattr(request.user, 'is_teacher') or not request.user.is_teacher:
        return render(request, "403.html", status=403)
    
    # Fetch unread notifications for the teacher
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notification.count()
    return render(request, "Teachers/teacher-dashboard.html", {
        'unread_notification_count': unread_notification_count,})


User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_admin

# ------------------ DEPARTMENT ------------------

@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'Academic/departments.html', {'departments': departments})


@login_required
@user_passes_test(is_admin)
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        hod_id = request.POST.get('hod')
        start_date = request.POST.get('start_date')
        hod = User.objects.get(id=hod_id) if hod_id else None

        Department.objects.create(name=name, hod=hod, start_date=start_date)
        return redirect('department_list')

    teachers = User.objects.filter(is_teacher=True)
    return render(request, 'Academic/add-department.html', {'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        department.name = request.POST.get('name')
        hod_id = request.POST.get('hod')
        department.hod = User.objects.get(id=hod_id) if hod_id else None
        department.start_date = request.POST.get('start_date')
        department.save()
        return redirect('department_list')

    teachers = User.objects.filter(is_teacher=True)
    return render(request, 'Academic/edit-department.html', {'department': department, 'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    # return render(request, 'academic/confirm_delete.html', {'object': department, 'type': 'Department'})


# ------------------ SUBJECT ------------------

@login_required
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'Academic/subjects.html', {'subjects': subjects})


@login_required
@user_passes_test(is_admin)
def subject_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        class_name = request.POST.get('class_name')
        Subject.objects.create(name=name, class_name=class_name)
        return redirect('subject_list')
    return render(request, 'Academic/add-subject.html')


@login_required
@user_passes_test(is_admin)
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.class_name = request.POST.get('class_name')
        subject.save()
        return redirect('subject_list')

    return render(request, 'Academic/edit-subject.html', {'subject': subject})


@login_required
@user_passes_test(is_admin)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    # return render(request, 'academic/confirm_delete.html', {'object': subject, 'type': 'Subject'})