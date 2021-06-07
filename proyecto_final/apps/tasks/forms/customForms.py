from django import forms
from django.db.models.fields import EmailField
from ..models import User


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), required=True)

    def login(self, request):
        email= self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.authenticate(email, password)
        if user == None:
            raise forms.ValidationError("Contraseña Incorrecta")   

        return user

    def clean(self):
        cleaned_data = super().clean()
        user_exists = User.user_exists(cleaned_data.get("email"))
        if not user_exists:
            raise forms.ValidationError("Usuario no registrado")    
