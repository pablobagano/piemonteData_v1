from django.contrib import admin
from .models import Diretor, Gerente, Supervisor, Agente, UserProfile
# Register your models here.

admin.site.register(Diretor)
admin.site.register(Gerente)
admin.site.register(Supervisor)
admin.site.register(Agente)
admin.site.register(UserProfile)