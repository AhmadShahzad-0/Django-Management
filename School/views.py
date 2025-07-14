from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Subject, Notification
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse, HttpResponseForbidden

# Create your views here.
def index(request):
    return render(request, "Home/index.html", {})

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

# Add Department
def add_department(request):
    if request.method == 'POST':
        department_id = request.POST.get('department_id')
        name = request.POST.get('name')
        head_of_department = request.POST.get('head_of_department')
        start_date = request.POST.get('start_date')
        number_of_students = request.POST.get('number_of_students')

        if Department.objects.filter(department_id=department_id).exists():
            messages.error(request, "Department ID already exists.")
        else:
            Department.objects.create(
                department_id=department_id,
                name=name,
                head_of_department=head_of_department,
                start_date=start_date,
                number_of_students=number_of_students
            )
            messages.success(request, "Department added successfully.")
            return redirect('list_departments')

    return render(request, 'Departments/add-department.html')


# List Departments
def list_departments(request):
    departments = Department.objects.all()
    return render(request, 'Departments/departments.html', {'departments': departments})

# Edit Department
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        department.department_id = request.POST.get('department_id')
        department.name = request.POST.get('name')
        department.head_of_department = request.POST.get('head_of_department')
        department.start_date = request.POST.get('start_date')
        department.number_of_students = request.POST.get('number_of_students')

        department.save()
        messages.success(request, "Department updated successfully.")
        return redirect('list_departments', pk=pk)

    return render(request, 'Departments/edit-department.html', {'department': department})


# Delete Department
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect('list_departments')

# Add Subject
def add_subject(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        subject_class = request.POST.get('subject_class')

        Subject.objects.create(
            subject_id=subject_id,
            subject_name=subject_name,
            subject_class=subject_class
        )
        return redirect('list_subjects')
    return render(request, 'Subjects/add-subject.html')

# List Subjects
def list_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'Subjects/subjects.html', {'subjects': subjects})

# Edit Subject
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        subject.subject_id = request.POST.get('subject_id')
        subject.subject_name = request.POST.get('subject_name')
        subject.subject_class = request.POST.get('subject_class')
        subject.save()
        return redirect('list_subjects')

    return render(request, 'Subjects/edit-subject.html', {'subject': subject})

# Delete Subject
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return redirect('list_subjects')