from django import forms
from .models import * 
from django.core.exceptions import ValidationError
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