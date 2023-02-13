from django import forms
from endereco.models import Perfil_Endereco

class Perfil_EndercoForm(forms.ModelForm):
    class Meta:
        model = Perfil_Endereco
        fields = ('__all__')
        exclude = ('user_perfil',)