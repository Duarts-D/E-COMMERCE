from django.db import models

class Perfil_Endereco(models.Model):
        ESTADO =(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),)
   
        LOCAL = (
                ('CS','CASA'),
                ('TR','TRABALHO'),
                )
        #user_perfil = models.ForeignKey(Perfil_Usuario,on_delete=models.CASCADE)
        nome_completo = models.CharField(max_length=300)
        cep = models.CharField(max_length=8)
        estado = models.CharField(max_length=2,choices=ESTADO)
        cidade =  models.CharField(max_length=300)
        bairro =  models.CharField(max_length=300)
        rua_avenida = models.CharField(max_length=300)
        numero =  models.CharField(max_length=50,blank=True,null=True)
        complemento =  models.CharField(max_length=300,blank=True,null=True)
        trabalho_casa = models.CharField(max_length=2,default=LOCAL)
        telefone =  models.CharField(max_length=1)
        infomacao = models.CharField(max_length=300,blank=True,null=True)

        def __str__(self):
                return self.nome_completo