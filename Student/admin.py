from django.contrib import admin
from . models import Parent, Student

# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    list_filter = ('father_name', 'mother_name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'gender', 'student_id',
        'date_of_birth', 'student_class', 'joining_date',
        'student_mobile', 'admission_number', 'section',
        'get_department', 'get_parent'
    )
    search_fields = (
        'first_name', 'last_name', 'student_id',
        'student_class', 'admission_number', 'parent__father_name', 'parent__mother_name'
    )
    list_filter = ('gender', 'student_class', 'section', 'department')
    readonly_fields = ('slug', 'student_image_preview')
    autocomplete_fields = ['parent', 'subjects', 'department']

    fieldsets = (
        ('Basic Info', {
            'fields': ('first_name', 'last_name', 'student_id', 'slug')
        }),
        ('Personal Details', {
            'fields': ('gender', 'date_of_birth', 'religion', 'student_mobile')
        }),
        ('Admission Info', {
            'fields': ('joining_date', 'admission_number', 'student_class', 'section', 'department', 'subjects')
        }),
        ('Parent Info', {
            'fields': ('parent',)
        }),
        ('Media', {
            'fields': ('student_image', 'student_image_preview')
        }),
    )

    def get_department(self, obj):
        return obj.department.name if obj.department else "-"
    get_department.short_description = "Department"

    def get_parent(self, obj):
        return str(obj.parent)
    get_parent.short_description = "Parent"

    def student_image_preview(self, obj):
        if obj.student_image:
            return f'<img src="{obj.student_image.url}" width="80" height="80" style="object-fit: cover; border-radius: 6px;" />'
        return "(No Image)"
    student_image_preview.allow_tags = True
    student_image_preview.short_description = "Preview"