from django import forms
from django.forms import widgets
from ..models import Task
import datetime

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'due_date', 'completed']
        due_date = forms.DateField(
                widget=forms.DateInput(
                    attrs={
                        'input_format' : "%m/%d/%Y",
                        'placeholder' : 'mm-dd-AAAA',
                        'autocomplete' : 'off',
                        'id' : 'datepicker-duedate'
                    }
                )
             )

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
            raise forms.ValidationError("La fecha no puede ser en el pasado")