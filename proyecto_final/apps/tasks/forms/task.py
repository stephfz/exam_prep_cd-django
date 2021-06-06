from django import forms
from django.forms import widgets
from ..models import Task
import datetime

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'due_date', 'completed'] #"__all__"
        widgets = {
            'completed' : forms.CheckboxInput()
        }
        labels ={
            'name': 'Tarea',
            'due_date' : 'Fecha Limite',
            'completed' : 'Completado'
        }

    def clean(self):
        date = self.cleaned_data['due_date']
        if date < datetime.date.today():
            raise forms.ValidationError("La fecha no puede estar en el pasado") 
