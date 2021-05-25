from django import forms
from django.forms import widgets
from ..models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'due_date', 'completed']
        widgets = {
            'completed' : forms.CheckboxInput()
        }
        labels ={
            'name': 'Tarea',
            'due_date' : 'Fecha Limite',
            'completed' : 'Completado'
        }
