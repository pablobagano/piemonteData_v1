from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import UserProfile, Gerente, Supervisor, Agente
from .utils import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


# Create your views here.
def index(request):
    return HttpResponse('<h1>Hi</h1>')

@login_required
def UserDataView(request):
    try:
        current_user = get_object_or_404(UserProfile, user = request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse("UserProfile does not exist", status=404)
    role = current_user.cargo

    if role == 'diretor':
        gerentes = Gerente.objects.all()
        supervisores = Supervisor.objects.all()
        agentes = Agente.objects.all()

        gerentes_data = [model_to_dict(gerente) for gerente in gerentes]
        supervisores_data = [model_to_dict(supervisor) for supervisor in supervisores]
        agentes_data = [model_to_dict(agente) for agente in agentes]

        users = gerentes_data + supervisores_data + agentes_data

    elif role == 'gerente':
        manager_id = get_object_or_404(Gerente, id=current_user.root_id)
        supervisores = Supervisor.objects.filter(gerente = manager_id)
        agentes = Agente.objects.filter(gerente = manager_id)
        users = [
            {'nome': f'{agente.nome} {agente.sobrenome}', 'cargo': agente.cargo, 'gerente': agente.gerente.nome, 
             'supervisor':agente.supervisor.nome, 'matricula': agente.matricula,  
            'cidade': agente.cidade} for agente in agentes
        ] + [
            {'nome': f'{supervisor.nome} {supervisor.sobrenome}', 
             'cargo':supervisor.cargo, 
             'gerente': supervisor.gerente.nome, 'matricula': supervisor.matricula}
            for supervisor in supervisores]
    elif role == 'supervisor':
        supervisor_id = get_object_or_404(Supervisor, id = current_user.root_id)
        agentes = Agente.objects.filter(supervisor = supervisor_id)
        users = [{'nome': f'{agente.nome} {agente.sobrenome}', 'cargo': agente.cargo, 'gerente': agente.gerente, 
             'supervisor':agente.supervisor,  'matricula': agente.matricula, 
            'cidade': agente.cidade}  for agente in agentes]
    else: 
        users = []
    return JsonResponse({'users': users})