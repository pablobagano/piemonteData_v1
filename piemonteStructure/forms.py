from django import forms
from .models import * 
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
import re

class GerenteForm(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = {'nome', 'sobrenome', 'matricula', 'cargo', 'ativo', 'email'}
        labels = {
            'nome': 'Nome',
            'sobrenome' : 'Sobrenome',
            'matricula' : 'Matricula',
            'cargo' : 'Cargo',
            'ativo' : 'Em atividade', 
            'email' : 'E-mail'
        }
    
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        if not nome.is_alpha():
            raise ValidationError("O nome deve conter apenas letras")
        return nome
    
    def clean_sobrenome(self):
        sobrenome = self.cleaned_data['sobrenome']
        if not sobrenome.is_alpha():
            raise ValidationError("O nome deve conter apenas letras")
        return sobrenome
    
    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        pattern = r'^[A-Za-z]{1,2}\d{6,7}$'
        regex = re.compile(pattern)
        if not regex.match(matricula):
            raise ValidationError("Matrícula inválida")
        return matricula
    

class CustomLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
    
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code = 'invalid_login',
                    params={'username':self.username_field.verbose_name}, 
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data