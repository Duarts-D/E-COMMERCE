from django.db import models
from apps.usuario.models import Perfil_Usuario
from apps.endereco.choices import ESTADO,LOCAL


class Perfil_Endereco(models.Model):

        user_perfil = models.ForeignKey(Perfil_Usuario,on_delete=models.CASCADE)
        nome_completo = models.CharField(max_length=300)
        cep = models.CharField(max_length=8)
        estado = models.CharField(max_length=2,choices=ESTADO)
        cidade =  models.CharField(max_length=300)
        bairro =  models.CharField(max_length=300)
        rua_avenida = models.CharField(max_length=300)
        numero =  models.CharField(max_length=50,blank=True,null=True)
        complemento =  models.CharField(max_length=300,blank=True,null=True)
        trabalho_casa = models.CharField(max_length=2,choices=LOCAL,default='CS')
        telefone =  models.CharField(max_length=11)
        infomacao = models.TextField(max_length=150,blank=True,null=True)

        def __str__(self):
                return self.nome_completo