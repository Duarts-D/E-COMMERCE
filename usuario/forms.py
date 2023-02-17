from django import forms
from django.contrib.auth.models import User
from usuario.models import Perfil_Usuario
from django.core.validators import EmailValidator

import re


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password','email',)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil_Usuario
        fields = ('__all__')
        exclude = ('user',)

    nome = forms.CharField(
        label='Nome',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class":"form-control form-control-lg"
                }
                )
            )
    
    sobrenome = forms.CharField(
        label='Sobrenome',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class":"form-control form-control-lg"
            }
            )
        )

    data_de_nascimento = forms.CharField(  
        label='Data de Nascimento',
        required=True,
        max_length=8,
        widget=forms.DateInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"ex : 01/05/1990"}
        )
    )
    email = forms.CharField(        
        label='Email',
        required=True,
        validators=[EmailValidator],
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Ex: JaoJao@email.com"}
        )
    )
    telefone = forms.CharField(       
        label='Telefone',
        required=True,
        max_length=11,
        widget=forms.TimeInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":" ex :99 9 9999-5555"}
        )
    )
    cpf = forms.CharField(        
        label='CPF',
        required=True,
        max_length=11,
        widget=forms.TextInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Digite os 11 digito sem pontuação"}
        )
    )
    senha = forms.CharField(        
        label='Senha',
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Senha"}
        )
    )
    senha2 = forms.CharField(        
        label='Repetir senha',
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Digite novamente"}
        )
    )

    def clean(self,*args,**kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msg = {}

        nome_data = cleaned.get('nome')
        sobrenome_data = cleaned.get('sobrenome')
        data_de_nascimento_data = cleaned.get('data_de_nascimento')
        email_data = cleaned.get('email')
        telefone_data = cleaned.get('telefone')
        cpf_data = cleaned.get('cpf')
        senha_data = cleaned.get('senha')
        senha2_data = cleaned.get('senha2')


        msg_error_crct_especiais = 'Campo nao pode conter caracters especais'
        msg_error_espaços_vazio = 'Campo nao pode ter espaços'

        user = User.objects.filter(username=cpf_data).first()
        email = User.objects.filter(email=email_data).first()

        if nome_data:
            nome_data = nome_data.title()
            cleaned['nome'] = nome_data
            
            if re.search(r'[^a-zA-Z0-9\s]', nome_data):
                validation_error_msg['nome'] = msg_error_crct_especiais

            if any( x.isdigit() for x in nome_data):
                validation_error_msg['nome'] = 'Nome nao pode conter numeros.'
                
        if sobrenome_data:
            sobrenome_data = sobrenome_data.title()
            cleaned['sobrenome'] = sobrenome_data
            
            if re.search(r'[^a-zA-Z0-9\s]', sobrenome_data):
                validation_error_msg['sobrenome'] = msg_error_crct_especiais

            if any( x.isdigit() for x in sobrenome_data):
                validation_error_msg['sobrenome'] = 'Sobrenome nao pode conter numeros.'
        
        if data_de_nascimento_data:
            if re.search(r'[^a-zA-Z0-9\s]', data_de_nascimento_data):
                validation_error_msg['data_de_nascimento'] = msg_error_crct_especiais
            
            if len(data_de_nascimento_data)<8:
                validation_error_msg['data_de_nascimento'] = 'Data de nacimento incompleta'

            if ' ' in data_de_nascimento_data:
                validation_error_msg['data_de_nascimento'] = msg_error_espaços_vazio

            if any( x.isalpha() for x in data_de_nascimento_data):
                validation_error_msg['data_de_nascimento'] = 'Favor digite somente numero "ex: 08031994".'
        
        if email_data:
            email_data = email_data.lower()
            cleaned['email'] = email_data
            if email:
                validation_error_msg['email'] = 'Email já utilizado.'
            if ' ' in email_data:
                validation_error_msg = msg_error_espaços_vazio



        if telefone_data:
            if len(telefone_data) < 11:
                validation_error_msg['telefone'] = 'Numero de telefone incompleto'

            if ' ' in telefone_data:
                validation_error_msg['telefone']= msg_error_espaços_vazio            
            
            if re.search(r'[^0-9\s]', telefone_data):
                validation_error_msg['telefone'] = 'Favor digite somente numero "ex: 99 9 99999999".'
        
        if cpf_data:
            if re.search(r'[^0-9\s]', cpf_data):
                validation_error_msg['cpf'] = 'Favor digite somente numero "ex: 999.999.999-99".'
            
            if len (cpf_data) < 11:
                validation_error_msg['cpf'] = 'CPF incompleto.'

            if ' ' in cpf_data:
                validation_error_msg['cpf'] = 'CPF nao pode conter espaços vazios.'
            
            #TODO colocar validador de pcf : 
            #    
            
            if user:
                validation_error_msg['cpf'] = 'CPF Já utilizado.'
            


        if senha_data:
            if len(senha_data) < 8:
                validation_error_msg['senha'] = 'Senha muito curta, precisa ter mais de "8 digitos/letras".'

            if ' ' in senha_data:
                validation_error_msg['senha'] = msg_error_espaços_vazio
            
            if not any(x.isupper() for x  in senha_data ):
                validation_error_msg['senha'] = 'Senha dever conter "1 Letra Maisculo".'

            if not any(x.islower() for x in senha_data ):
                validation_error_msg['senha'] = 'Senha dever conter "1 Letra Minuscula".'

            if not (x.isdigit() for x in senha_data ):
                validation_error_msg['senha'] = 'Senha dever conter 1 numero.'
        
        if senha2_data and senha_data:
            if senha2_data != senha_data:
                validation_error_msg['senha2'] = 'Senha nao sao iguais.'

        if validation_error_msg:
            raise(forms.ValidationError(validation_error_msg))        

        
        return cleaned
        