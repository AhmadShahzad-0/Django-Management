from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_student, name='add_student'),
    path("list/", views.student_list, name='student_list'),
    path("students/<str:slug>/", views.view_student, name='view_student'),
]