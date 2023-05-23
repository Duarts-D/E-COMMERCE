from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.categoria