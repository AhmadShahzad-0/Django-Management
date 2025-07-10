from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/', views.list_departments, name='list_departments'),
    path('departments/<int:pk>/edit/', views.edit_department, name='edit_department'),
    path('departments/<int:pk>/delete/', views.delete_department, name='delete_department'),
]