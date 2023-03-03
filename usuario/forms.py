from django import forms
from django.contrib.auth.models import User
from usuario.models import Perfil_Usuario
from django.core.validators import EmailValidator
from utilidade.validador_cpf import valida_cpf
from utilidade.validators.validators import (caract_especiais_validador,
                                             string_validador,
                                             tamanho_len_validador)
from utilidade.validators.validators import (espaços_vazio_validador,
                                             digitos_validador,
                                             string_uma_maiscula_validador,
                                             string_uma_minuscula_validador)
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm


class SenhaResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(        
        label='Senha Nova',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Senha Nova",
            'type':'password'}
        )
    )
    new_password2 = forms.CharField(        
        label='Repetir Senha',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Digite Novamente",
            'type':'password'}
        )
    )
    def clean(self):
        cleaned = self.cleaned_data
        validation_error_msg = {}
        password2 = cleaned.get('new_password2')
        
        print(password2)
        msg_error_espaços_vazio = 'Nao pode conter espaços vazios'

        if password2:
            if espaços_vazio_validador(password2):
                validation_error_msg['new_password2'] = msg_error_espaços_vazio
            
            if not string_uma_maiscula_validador(password2):
                validation_error_msg['new_password2'] = 'Senha dever conter "1 Letra Maisculo".'

            if not string_uma_minuscula_validador(password2):
                validation_error_msg['new_password2'] = 'Senha dever conter "1 Letra Minuscula".'

            if not digitos_validador(password2):
                validation_error_msg['new_password2'] = 'Senha dever conter 1 numero.'        
        
        if validation_error_msg:
                raise(forms.ValidationError(validation_error_msg))
        
        return cleaned
    field_order = ["old_password", "new_password1", "new_password2"]

class AlterarSenhaForm(SenhaResetConfirmForm):

    old_password = forms.CharField(        
        label='Senha Antiga',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Senha",
            'type':'password'}
        )
    )

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')

    


class SenhaEmailResetForm(PasswordResetForm):
    email = forms.EmailField(        
        label='Email',
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Senha",
            'type':'email'}
        )
    )
    class Meta:
        model = User
        fields = ('email')


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil_Usuario
        fields = ('__all__')
        exclude = ('user',)


    def __init__(self, usuario=None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.usuario = usuario
        valor_inicial = kwargs.pop('valor_inicial', None)
        super().__init__(*args, **kwargs)
        if valor_inicial is not None:
            self.fields['email'].initial = valor_inicial

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



        msg_error_crct_especiais = 'Campo nao pode conter caracters especais'
        msg_error_espaços_vazio = 'Campo nao pode ter espaços'

        user = User.objects.filter(username=self.usuario).first()
        perfil_email = Perfil_Usuario.objects.filter(email=email_data).first()

        cpf_enviado = Perfil_Usuario.objects.filter(cpf=cpf_data).first()

        if self.usuario:
            if perfil_email:
                    if perfil_email is not None and perfil_email.user.pk != user.pk:
                        validation_error_msg['email'] = 'Email ja utilizado'
                 
            if cpf_enviado:
                if cpf_enviado is not None and cpf_enviado.user.pk != user.pk:
                        validation_error_msg['cpf'] = 'Cpf ja utilizado'
            
        if nome_data:
            nome_data = nome_data.title()
            cleaned['nome'] = nome_data
            
            if caract_especiais_validador(nome_data):
                validation_error_msg['nome'] = msg_error_crct_especiais

            if string_validador(nome_data):
                validation_error_msg['nome'] = 'Nome nao pode conter numeros.'         

                    
            if sobrenome_data:
                sobrenome_data = sobrenome_data.title()
                cleaned['sobrenome'] = sobrenome_data
                
                if caract_especiais_validador(sobrenome_data):
                    validation_error_msg['sobrenome'] = msg_error_crct_especiais

                if string_validador(sobrenome_data):
                    validation_error_msg['sobrenome'] = 'Sobrenome nao pode conter numeros.'
            
            if data_de_nascimento_data:

                if tamanho_len_validador(data_de_nascimento_data,8):
                    validation_error_msg['data_de_nascimento'] = 'Data de nacimento incompleta'

                if espaços_vazio_validador(data_de_nascimento_data):
                    validation_error_msg['data_de_nascimento'] = msg_error_espaços_vazio

                if digitos_validador(data_de_nascimento_data):
                    validation_error_msg['data_de_nascimento'] = 'Favor digite somente numero "ex: 08031994".'
            
            if email_data:
                email_data = email_data.lower()
                cleaned['email'] = email_data


                if espaços_vazio_validador(email_data):
                    validation_error_msg = msg_error_espaços_vazio
                
                if not self.usuario:
                    if perfil_email:
                        validation_error_msg['email'] = 'Email já utilizado.'


            if telefone_data:
                
                if tamanho_len_validador(telefone_data,11):
                    validation_error_msg['telefone'] = 'Numero de telefone incompleto'

                if espaços_vazio_validador(telefone_data):
                    validation_error_msg['telefone']= msg_error_espaços_vazio            
                
                if digitos_validador(telefone_data):
                    validation_error_msg['telefone'] = 'Favor digite somente numero "ex: 99 9 99999999".'
                
            if cpf_data:
                if not valida_cpf(cpf_data):
                    validation_error_msg['cpf'] = 'CPF invalido'

            
                if digitos_validador(cpf_data):
                    validation_error_msg['cpf'] = 'Favor digite somente numero "ex: 999.999.999-99".'
                
                if tamanho_len_validador(cpf_data,11):
                    validation_error_msg['cpf'] = 'CPF incompleto.'

                if espaços_vazio_validador(cpf_data):
                    validation_error_msg['cpf'] = 'CPF nao pode conter espaços vazios.'
                
                #TODO colocar validador de pcf : 
                #    
                if not self.usuario:  
                    if cpf_enviado:
                        validation_error_msg['cpf'] = 'CPF Já utilizadoooo.'
            
        if validation_error_msg:
            raise(forms.ValidationError(validation_error_msg))                    

        return cleaned
    
class PasswordsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password','password2')

    password = forms.CharField(        
        label='Senha',
        required=False,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Senha"}
        )
    )
    password2 = forms.CharField(        
        label='Repetir senha',
        required=False,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Digite novamente"}
        )
    )   

    def clean(self):
        cleaned = self.cleaned_data
        validation_error_msg = {}
        senha_data = cleaned.get('password')
        senha2_data = cleaned.get('password2')

        msg_error_espaços_vazio = 'Nao pode conter espaços vazios'
        
            
        if senha_data and senha2_data:
            if tamanho_len_validador(senha2_data,8):
                validation_error_msg['password2'] = 'Senha muito curta, precisa ter mais de "8 digitos/letras".'

            if espaços_vazio_validador(senha2_data):
                validation_error_msg['password2'] = msg_error_espaços_vazio
            
            if not string_uma_maiscula_validador(senha2_data):
                validation_error_msg['password2'] = 'Senha dever conter "1 Letra Maisculo".'

            if not string_uma_minuscula_validador(senha2_data):
                validation_error_msg['password2'] = 'Senha dever conter "1 Letra Minuscula".'

            if not digitos_validador(senha2_data):
                validation_error_msg['password2'] = 'Senha dever conter 1 numero.'
    
        if senha2_data and senha_data:
            if senha2_data != senha_data:
                validation_error_msg['password2'] = 'Senha nao sao iguais.'


        if not senha_data:
            validation_error_msg['password'] = 'Campos nao pode fica vazio'
        if not senha2_data:
            validation_error_msg['password2'] = 'Campos nao pode fica vazio'         

        if validation_error_msg:
            raise(forms.ValidationError(validation_error_msg))

        return cleaned
    
