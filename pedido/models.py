from django.db import models
from django.contrib.auth.models import User
from pedido.choices import STATUS

# Create your models here.

class Pedido(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario')
    total = models.PositiveIntegerField(verbose_name='Total de Produtos')
    qtd_valor_total = models.FloatField(max_length=300,verbose_name='Valor Total')
    status = models.CharField(max_length=1,choices=STATUS,default='C')

    def __str__(self):
        return f'Pedido N. {self.pk}'

class Itempedido(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    produto = models.CharField(max_length=300)
    produto_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promo = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    def __str__(self):
        return f'Itens do {self.pedido} produto {self.produto}'
    
    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'