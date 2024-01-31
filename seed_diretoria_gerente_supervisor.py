import os, django 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','setup.settings')
django.setup()

from piemonteStructure.models import Diretor, Gerente, Supervisor, Agente
from django.contrib.auth.models import User
from time import sleep

def criar_diretor(nome, sobrenome, matricula, email):
    diretor = Diretor(nome=nome, sobrenome=sobrenome, matricula=matricula, email=email)
    diretor.save()
    print(f"{nome} ok")

def criar_gerente(diretor, nome, sobrenome, matricula, email):
    diretor= Diretor.objects.get(id=Diretor)
    gerente = Gerente(Diretor=diretor, nome=nome, sobrenome=sobrenome, matricula=matricula, email=email)
    gerente.save()
    print(f"{nome} ok") 

def criar_supervisor(diretor, gerente, nome, sobrenome, matricula, email):
    diretor= Diretor.objects.get(id=Diretor)
    gerente = Gerente.objects.get(id=gerente)
    supervisor = Supervisor(Diretor=diretor, gerente=gerente, nome=nome, sobrenome=sobrenome, matricula=matricula, email=email)
    supervisor.save()
    print(f"{nome} ok")

email = 'adm@piemontecred.com.br'

def password():
    superuser = User.objects.filter(is_superuser=True)    
    for user in User.objects.all():
        if not user in superuser:
            user.set_password('jacobina')
            user.save()
            print(f'{user.username}: Password created')


if __name__ == '__main__':

    try: 
        criar_diretor('Reinildo', 'Vilas Boas', 'RE123456', email)
        sleep(5)
        criar_diretor('Pablo', 'Bagano', 'PA123456', email)
        sleep(5)
        criar_gerente(2, 'Michelle', 'Cerqueira Donin', 'MI123456', email)
        sleep(5)
        criar_gerente(1, 'Charles', 'Jacobina', 'CH123456', email)
        sleep(5)
        criar_supervisor(1, 2, 'Milka', 'Jacobina', 'ML123456', email)
        sleep(5)
        criar_supervisor(2, 1, 'Rosangela', 'Cerqueira', 'JS123456', email)
        sleep(5)
        criar_supervisor(2, 2, 'Manoel', 'Gomes', 'MG123456', email)
        sleep(5)
        criar_supervisor(2, 1, 'Renata', 'Costa', 'MG123456', email)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")



    password()
