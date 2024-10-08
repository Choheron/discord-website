from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('getAllTodoItems', views.getAllToDo),
    path('createTodo', views.createTodo),
    path('bulkCreateTodo', views.bulkCreateTodo),
]
