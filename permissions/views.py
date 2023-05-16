from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User,Group,Permission
from rolepermissions.roles import get_user_roles
from rolepermissions.permissions import available_perm_status
from rolepermissions.permissions import grant_permission
from rolepermissions.roles import assign_role

class Permissoes(View):
    template_name = 'permissoses.html'
    def get(self,*args):
        funcionarios = User.objects.filter(is_staff=False,is_superuser=False)
        dados = {}
        for funcionario in funcionarios:
            permissao = available_perm_status(funcionario)
            grupo = get_user_roles(funcionario)

            for p,y in permissao.items():
                if y is True:
                    dados[funcionario.first_name] = p
        return render(self.request,self.template_name,{'funcionarios':funcionarios,'dados':dados})