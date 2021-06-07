from django import forms
from django.forms import widgets
from ..models import Task
import datetime

custom_errors = {
    'required': 'Requerido',
    'invalid': 'Fecha Invalida'
}

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(error_messages= custom_errors,
                widget=forms.DateInput(
                    attrs={
                        "type" : "date"                    
                    }
                ))
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
