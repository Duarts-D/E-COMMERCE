from django import forms
from django.contrib.auth.models import User
from usuario.models import Perfil_Usuario

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
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":"Ex: JaoJao@email.com"}
        )
    )
    telefone = forms.CharField(       
        label='Telefone',
        required=True,
        max_length=8,
        widget=forms.NumberInput(
            attrs={"class":"form-control form-control-lg",
            "phaceholder":" ex :99 9 9999-5555"}
        )
    )
    cpf = forms.CharField(        
        label='CPF',
        required=True,
        max_length=11,
        widget=forms.NumberInput(
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

