from django.contrib import admin
from apps.usuario.models import Perfil_Usuario


class PerfilUsuarioAdm(admin.ModelAdmin):
    list_display = ('nome','sobrenome',)

admin.site.register(Perfil_Usuario,PerfilUsuarioAdm)