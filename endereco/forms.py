from django import forms
from endereco.models import Perfil_Endereco
from endereco.choices import ESTADO,LOCAL

import re

class Perfil_EndercoForm(forms.ModelForm):
    class Meta:
        model = Perfil_Endereco
        fields = ('__all__')
        exclude = ('user_perfil',)

    nome_completo = forms.CharField(
    label='Nome Completo',
    required=True,
    max_length=100,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
        "style": "text-align: center;"
            }
            )
        )
    cep = forms.CharField(
    label='Cep',
    required=True,
    max_length=8,
    widget=forms.NumberInput(
        attrs={"class":"form-control form-control-lg",
             "style": "text-align: center;"}
            )
        )
    estado = forms.ChoiceField(
    label='Estado',
    required=True,
    choices=ESTADO,
    widget=forms.Select(
        attrs={"class" : "form-control form-control-lg",
        "style": "text-align: center;"}
            ),
        )
    


    cidade = forms.CharField(
    label='Cidade',
    required=True,
    max_length=100,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    bairro = forms.CharField(
    label='Bairro',
    required=True,
    max_length=100,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    rua_avenida = forms.CharField(
    label='Rua/Avenida',
    required=True,
    max_length=100,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    numero = forms.CharField(
    label='Numero',
    required=False,
    max_length=15,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    complemento = forms.CharField(
    label='Complemento',
    required=False,
    max_length=100,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    trabalho_casa = forms.ChoiceField(
    label='Local de Entrega',
    required=True,
    choices=LOCAL,
    widget=forms.Select(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    telefone = forms.CharField(
    label='Telefone',
    required=True,
    max_length=11,
    widget=forms.TextInput(
        attrs={"class":"form-control form-control-lg",
            "style": "text-align: center;"}
            )
        )
    infomacao = forms.CharField(
    label='Informaçao Adicional',
    required=False,
    max_length=100,
    widget=forms.Textarea(
        attrs={"class":"form-control form-control-lg",
        "style": "text-align: center;",
            "cols": 100,
            "rows": 5}
            )
        )

    def clean(self,*args,**kwargs):
        cleaned = self.cleaned_data
        validation_error_msg = {}

        msg_error_crct_especiais = 'Campo nao pode conter caracters especais'
        msg_error_espaços_vazio = 'Campo nao pode ter espaços'

        #email_data = email_data.lower()
        #cleaned['email'] = email_data

        nome_completo_data = cleaned.get('nome_completo')
        cep_data = cleaned.get('cep')
        cidade_data = cleaned.get('cidade')
        bairro_data = cleaned.get('bairro')
        rua_data = cleaned.get('rua')
        numero_data = cleaned.get('numero')
        complemento_data = cleaned.get('complemento')
        telefone_data = cleaned.get('telefone')


        if nome_completo_data:
            nome_completo_data = nome_completo_data.title()
            cleaned['nome_completo'] = nome_completo_data
            
            if re.search(r'[^a-zA-Z0-9\s]', nome_completo_data):
                validation_error_msg['nome_completo'] = msg_error_crct_especiais

            if any( x.isdigit() for x in nome_completo_data):
                validation_error_msg['nome_completo'] = 'Nome nao pode conter numeros.'         

        if cep_data:
            if re.search(r'[^0-9\s]', cep_data):
                validation_error_msg['cep'] = 'Favor digite somente numero "ex: 999.999.999-99".'
            
            if len (cep_data) < 8:
                validation_error_msg['cep'] = 'Cep incompleto.'

            if ' ' in cep_data:
                validation_error_msg['cep'] = 'CPF nao pode conter espaços vazios.'

        if cidade_data:
            cidade_data = cidade_data.title()
            cleaned['cidade'] = cidade_data
            if re.search(r'[^a-zA-Z0-9\s]', cidade_data):
                validation_error_msg['cidade'] = msg_error_crct_especiais

            if any( x.isdigit() for x in cidade_data):
                validation_error_msg['cidade'] = 'Nome nao pode conter numeros.'         
                
        if complemento_data:
            complemento_data = complemento_data.title()
            cleaned['complemento'] = complemento_data
        
        if telefone_data:
            if re.search(r'[^0-9]', telefone_data):
                validation_error_msg['telefone'] = 'Favor insira somente numeros'
            if len(telefone_data) < 11:
                validation_error_msg['telefone'] = 'Numero de telefone incompleto'

            if ' ' in telefone_data:
                validation_error_msg['telefone']= msg_error_espaços_vazio            
                
        if validation_error_msg:
            raise(forms.ValidationError(validation_error_msg))

        return cleaned