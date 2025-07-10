from django.shortcuts import render, get_object_or_404, redirect
from .models import Department
from django.contrib import messages
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, "Home/index.html", {})

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