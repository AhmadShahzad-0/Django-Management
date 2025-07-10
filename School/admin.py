from django.contrib import admin
from .models import Department, Subject

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'name', 'head_of_department', 'start_date', 'number_of_students')
    search_fields = ('department_id', 'name', 'head_of_department')
    list_filter = ('start_date',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name', 'subject_class')
