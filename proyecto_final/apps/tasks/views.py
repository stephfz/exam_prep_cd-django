
from collections import deque
import re

from django.db.models import query
from django.http.response import JsonResponse
from .models import Task, User
from django.shortcuts import render, redirect, resolve_url
from .forms.user import UserForm
from .forms.task import TaskForm
from .forms.customForms import LoginForm
from django.contrib import messages


from django.views.generic import ListView

from django.template.loader import render_to_string


class TasksListView(ListView):
    template_name = 'tasks-list.html'
    queryset = Task.objects.filter(completed = True).order_by('-due_date')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['logged_user_id']
        user = User.objects.get(id = int(user_id))
        context['user'] = user
        print (context)
        return context



def index(request):
    ##GET
    #mostrar form de login
    #mostrar form de register
    formRegister = UserForm()
    formLogin = LoginForm()
    return render(request, 'index.html', {'formRegister': formRegister, 'formLogin': formLogin})

def register(request):
    if request.method == 'GET':
        formRegister = UserForm()
    else:
        formRegister = UserForm(request.POST)
        if formRegister.is_valid():
            user = formRegister.save()
            request.session['logged_user'] = user.name
            request.session['logged_user_id'] = user.id
            return redirect("/home")
    formLogin = LoginForm()         
    return render(request, 'index.html', 
            {'formRegister': formRegister,'formLogin': formLogin})  

def login(request):
    if request.method == "GET":
        formLogin = LoginForm()
    else:
        formLogin = LoginForm(request.POST)
        if formLogin.is_valid():
            user = formLogin.login(request.POST)
            if user:
                request.session['logged_user'] = user.name
                request.session['logged_user_id'] = user.id
                return redirect("/home")
    formRegister = UserForm()
    return render(request, 'index.html',{'formLogin':formLogin, 'formRegister': formRegister} ) 

def logout(request):  
    try:
        del request.session['logged_user']
        del request.session['logged_user_id']
    except:
        print('Error')
    return redirect("/")                    

def home(request):
    try:
        user = User.objects.get(id = int(request.session['logged_user_id']))
        if user:
            #tareas pendientes , completed = False 
            tasks_pending = user.tasks.all().filter(completed = False).order_by('-due_date')
            #tareas mis completadas
            tasks_completed = user.tasks.all().filter(completed = True)

            return render(request, 'home.html', 
                            {'user': user, 
                            'tasks_pending': tasks_pending, 
                            'tasks_completed': tasks_completed})
        else:
            return redirect("/")
    except:
        return redirect("/")


def task(request):
    if request.method == "POST":
        #guardar el task
        user = User.objects.get(id = int(request.session['logged_user_id']))
        errors = Task.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, key)                               
            return redirect('/home')    
        else:    
            task = Task.objects.create(name = request.POST['name'], 
                                due_date = request.POST['due_date'],
                                user = user)
            tasks_pending = user.tasks.all().filter(completed = False).order_by('-due_date')                    
            context = {'tasks_pending': tasks_pending} 
            print (context)                   
            if request.is_ajax():
                html = render_to_string('user-tasks.html', context, request= request)
                print (html)  
                return JsonResponse({'form': html})  
        #return redirect("/home")   


def task_detail(request, task_id):
    task = Task.objects.get(id = int(task_id))
    formTask = TaskForm(instance = task)
    if request.method == "POST": #actualizar task
        formTask = TaskForm(request.POST, instance=task)
        if  "cancel" in request.POST:
            return redirect('/home')
        if formTask.is_valid():
            completed = request.POST.get('completed', '') == 'on'
            task.name = request.POST['name']
            task.completed = completed
            task.save() #actualizar task
            return redirect('/home')
    return render(request, 'task_detail.html' , {'formTask': formTask})

def like(request, task_id):
    results = Task.objects.filter(id=task_id)
    if len(results) > 0:
        task = results[0]
        user = User.objects.get(id=request.session['logged_user_id'])
        task.likes.add(user)
        return redirect('dashboard')         

        



