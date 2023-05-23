from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Perfil_Usuario(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE )
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    data_de_nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    cpf = models.CharField(max_length=11)
    
    class Meta:
        verbose_name = 'Perfil Usuario'
        verbose_name_plural = 'Perfils de Usuarios'
    
    def __str__(self):
        return self.nome

    @property
    def birthday(self):
        date_now = datetime.now()
        date_now = date_now.date()
        birthday = date_now.year - self.data_de_nascimento.year
        return birthday