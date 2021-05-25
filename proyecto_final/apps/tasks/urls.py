from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('home', views.home),
    path('task', views.task),
    path('task_detail/<int:task_id>', views.task_detail),
]