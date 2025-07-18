from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('notification/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read' ),
    path('notification/clear-all', views.clear_all_notification, name= "clear_all_notification"),
    # Department URLs
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<int:pk>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:pk>/delete/', views.delete_department, name='delete_department'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/', views.list_subjects, name='list_subjects'),
    path('subjects/<int:pk>/edit/', views.edit_subject, name='edit_subject'),
    path('subjects/<int:pk>/delete/', views.delete_subject, name='delete_subject'),
]