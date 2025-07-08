from django.contrib import admin
from django.utils.html import format_html
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'teacher_class', 'teacher_gender', 'teacher_subject', 'teacher_section', 'teacher_mobile', 'teacher_address', 'image_preview')
    search_fields = ('teacher_id', 'teacher_name', 'teacher_subject', 'teacher_mobile')
    list_filter = ('teacher_gender', 'teacher_class', 'teacher_section')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.teacher_image:  # assuming image field is named teacher_image
            return format_html('<img src="{}" width="70" style="border-radius: 50%;" />', obj.teacher_image.url)
        return "No Image"
    
    image_preview.short_description = 'Profile Image'
