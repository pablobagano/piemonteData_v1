from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from info import * 
from .utils import create_user_send_email

# Create your models here.
"""
This project is developed for Piemonte Group, a company in the financial business. 
The class Diretoria, Gerencia, Supervisao and Agentes represent different hierarchical levels. Respectively Directors, Managers, Supervisors and Agents. 
Each class has standard attribuites, such as nome(name), sobrenome(last name), matricula (ID) and email.
Each object will also become a user to the platform, in which each hierachical level will hold differente access priveleges. 
All the objects are vertically connected through ForeignKey relationships. This design's intention is to reflect the company's organizational structure

Special Features:
- Custom save methods for automated user creation and email notifications.
- Hierarchical data integrity ensured through Django's ORM.

This structure allows for a clear representation of the company's hierarchy and efficient user management within the platform.
"""

class Diretor(models.Model):
    nome = models.CharField(max_length = 20, null=False, blank=False)
    sobrenome = models.CharField(max_length = 30, null=False, blank=False)
    matricula = models.CharField(max_length = 20, null=False, blank=False)
    cargo = models.CharField(max_length = 20, default = 'diretor')
    email = models.EmailField()
    email_sent = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        email_sent_before_save = self.email_sent
        super(Diretor, self).save(*args, **kwargs)
        user_creation, new_user = create_user_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.root_id = self.id
        new_user.save()

        if user_creation and not email_sent_before_save:
            self.email_sent = True
            super(Diretor, self).save(*args, **kwargs)


class Gerente(models.Model):
    nome = models.CharField(max_length = 20, null=False, blank=False)
    sobrenome = models.CharField(max_length = 30, null=False, blank=False)
    matricula = models.CharField(max_length = 20, null=False, blank=False)
    cargo = models.CharField(max_length = 20, default = 'gerente')
    ativo = models.BooleanField(default=True)
    email = models.EmailField()
    email_sent = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        email_sent_before_save = self.email_sent
        super(Gerente, self).save(*args, **kwargs)
        user_creation, new_user = create_user_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.root_id = self.id
        new_user.save()

        if user_creation and not email_sent_before_save:
            self.email_sent = True
            super(Gerente, self).save(*args, **kwargs)

class Supervisor(models.Model):
    nome = models.CharField(max_length = 20, null=False, blank=False)
    sobrenome = models.CharField(max_length = 30, null=False, blank=False)
    matricula = models.CharField(max_length = 20, null=False, blank=False)
    cargo = models.CharField(max_length = 20, default = 'supervisor')
    gerente = models.ForeignKey(Gerente, on_delete = models.SET_NULL, null = True)
    ativo = models.BooleanField(default = True)
    email = models.EmailField()
    email_sent = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def save(self, *args, **kwargs):
        email_sent_before_save = self.email_sent
        super(Supervisor, self).save(*args, **kwargs)
        user_creation, new_user = create_user_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.root_id = self.id
        new_user.gerente = self.gerente
        new_user.save()

        if user_creation and not email_sent_before_save:
            self.email_sent = True
            super(Supervisor, self).save(*args, **kwargs)
        


class Agente(models.Model):
    nome = models.CharField(max_length = 20, null=False, blank=False)
    sobrenome = models.CharField(max_length = 30, null=False, blank=False)
    matricula = models.CharField(max_length = 20, null=False, blank=False)
    cargo = models.CharField(max_length = 20, default = 'agente')
    gerente = models.ForeignKey(Gerente, on_delete = models.SET_NULL, null = True)
    supervisor = models.ForeignKey(Supervisor, on_delete = models.SET_NULL, null = True)
    cidade = models.CharField(max_length=50, choices = lista_cidades, null = False, blank = False)
    ativo = models.BooleanField(default = True)
    email = models.EmailField(null=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    def save(self, *args, **kwargs):
        if self.supervisor and not self.gerente:
            self.gerente = self.supervisor.gerente
        email_sent_before_save = self.email_sent
        super(Agente, self).save(*args, **kwargs)
        user_creation, new_user = create_user_send_email(self.nome, self.sobrenome, self.cargo, self.email)
        new_user.root_id = self.id
        new_user.gerente = self.gerente
        new_user.supervisor = self.supervisor
        new_user.save()

        if user_creation and not email_sent_before_save:
            self.email_sent = True
            super(Agente, self).save(*args, **kwargs)
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT, null=False)
    nome = models.CharField(max_length = 20, null=False, blank=False)
    sobrenome = models.CharField(max_length = 30, null=False, blank=False)
    root_id = models.IntegerField(null = True, blank = True)
    cargo = models.CharField(max_length=15, null=False, blank=False, default=None)
    gerente = models.ForeignKey(Gerente, on_delete = models.SET_NULL, null = True, blank = True)
    supervisor = models.ForeignKey(Supervisor, on_delete = models.SET_NULL, null = True, blank = True)
    password_needs_change = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}: {self.user.username}"
    
    def diretoria(self):
        return self.role == 'diretor'
    
    def gerencia(self):
        return self.role == 'gerente'
    
    def supervisao(self):
        return self.role == 'supervisor'
    
    def agente(self):
        return self.role == 'agente'