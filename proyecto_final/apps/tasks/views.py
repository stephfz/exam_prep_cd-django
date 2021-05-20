
from collections import deque
import re
from .models import Task, User
from django.shortcuts import render, redirect, resolve_url
from .forms.user import UserForm
from .forms.customForms import LoginForm

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
            return redirect("/home")
    formLogin = LoginForm()         
    return render(request, 'index.html', {'formRegister': formRegister,'formLogin': formLogin})  


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
        print('Erorr')
    return redirect("/")                    

def home(request):
    user = User.objects.get(id = int(request.session['logged_user_id']))
    return render(request, 'home.html', {'user': user})

def task(request):
    if request.method == "POST":
        #guardar el task
        user = User.objects.get(id = int(request.session['logged_user_id']))
        task = Task.objects.create(name = request.POST['name'], 
                            due_date = request.POST['due_date'],
                            user = user)
        return redirect("/home")                    