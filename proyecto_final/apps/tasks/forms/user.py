from django import forms
from django.forms.widgets import ClearableFileInput

from ..models import User

my_default_errors = {
    'required': 'Requerido',
    'invalid': 'Fecha Invalida'
}

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label = 'Confirmar Contraseña'
    )
    fecha_nacimiento = forms.DateField(error_messages= my_default_errors,
                widget=forms.DateInput(
                    attrs={
                        "type" : "date"                    
                    }
                )
    )
    class Meta:
        model = User
        fields = ['name','lastname','email', 'fecha_nacimiento', 'password']
        widgets = {
            'name' : forms.TextInput(attrs={'placeholder': 'Nombres Completos'}),
            'password' : forms.PasswordInput(),
        }
        labels = {
           'name': "Nombres",
           'lastname': "Apellidos",
           'fecha_nacimiento': "Fecha de Nacimiento",
           'email': "Correo Electronico",
           'password': "Contraseña",
        }

    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if (password != confirm_password):
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )
        user_exists = User.user_exists(cleaned_data.get("email"))
        if user_exists:
            raise forms.ValidationError("El usuario ya existe")
            