from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class Perfil_Usuario(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE )
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    data_de_nascimento = models.CharField(max_length=8)
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    cpf = models.CharField(max_length=11)
    
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Perfil Usuario'
        verbose_name_plural = 'Perfils de Usuarios'