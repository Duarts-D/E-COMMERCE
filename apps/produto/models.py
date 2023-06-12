from django.db import models
from django.utils.text import slugify

class Produto(models.Model):
    CATEGORIAS = (
                ('CPU','Computadores'),
                ('PLC','Placa Mãe'),
                ('PRC','Processadores'),
                ('MMR','Memoria Ram'),
                ('GAB','Gabinites'),
                ('KIT','Kits Gamers'),
                ('FOT','Fontes'),
                ('GPU','Placa de Video'),
                
                )

    nome = models.CharField(max_length=200)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    descricao_longa = models.TextField(max_length=1000)
    estoque = models.PositiveIntegerField(default=1)
    imagem = models.ImageField(upload_to='media/%Y/%m/%d',blank=True,null=True)
    publico = models.BooleanField(default=False)
    slug = models.SlugField(unique=True,blank=True,max_length=300)
    categoria = models.CharField(max_length=3,choices=CATEGORIAS,default='CPU')
    peso = models.FloatField(default=0,blank=True,null=True)
    comprimento = models.FloatField(default=0,blank=True,null=True)
    altura = models.FloatField(default=0,blank=True,null=True)
    largura = models.FloatField(default=0,blank=True,null=True)

    objects = models.Manager()

    def save(self,*args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.nome
        
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

class Modelo(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200,blank=True,null=False)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    descricao_curta = models.TextField(max_length=200,blank=True,null=True)
    estoque = models.PositiveIntegerField(default=1)

    def save(self,*args, **kwargs):
        if self.nome == None or '':
            nome = self.produto.nome
            self.nome = nome
        super().save(*args,**kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'