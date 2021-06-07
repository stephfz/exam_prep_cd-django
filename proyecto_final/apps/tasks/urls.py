from django.urls import path, include
from . import views
from .views import TasksListView



urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('home', views.home),
    path('task', views.task),
    path('task_detail/<int:task_id>', views.task_detail),
    path('like/<int:task_id>', views.like, name='like'),
    path('task', views.task),
    path('dashboard', TasksListView.as_view(), name="dashboard"),
]