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
    widget=forms.NumberInput(
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
        validation_error = {}

        telefone_data = cleaned.get('telefone')

        if telefone_data:
            if re.search(r'[^0-9]', telefone_data):
                validation_error['telefone'] = 'Favor insira somente numeros'

        if validation_error:
            raise(forms.ValidationError(validation_error))

        return cleaned