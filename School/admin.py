from django.contrib import admin
from .models import Department, Subject, Notification

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'hod', 'start_date', 'num_students_display')
    search_fields = ('name', 'hod__username', 'hod__first_name', 'hod__last_name')
    list_filter = ('start_date',)
    autocomplete_fields = ['hod']

    def num_students_display(self, obj):
        return obj.num_students()
    num_students_display.short_description = "No. of Students"

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name')
    search_fields = ('name', 'class_name')
    list_filter = ('class_name',)

admin.site.register(Notification)